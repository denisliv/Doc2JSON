import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Union

pipelines_dir = os.path.dirname(os.path.abspath(__file__))
if pipelines_dir not in sys.path:
    sys.path.insert(0, pipelines_dir)

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ocr_utils.config import AppConfig
from ocr_utils.file_utils import download_pdfs_to_temp_paths
from ocr_utils.markdown_utils import html_to_markdown_with_tables
from ocr_utils.prompts import PROMPT_TEMPLATE
from ocr_utils.schemas import enrich_json, format_instructions, output_parser
from ocr_utils.text_utils import (
    remove_parentheses_around_numbers,
    truncate_after_diluted_eps,
)
from paddleocr import PaddleOCRVL
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class Pipeline:
    """
    Pipeline для OpenWebUI: PDF → PaddleOCRVL → Markdown → LLM → JSON.
    """

    class Valves(BaseModel):
        LLM_API_URL: str
        LLM_API_KEY: str
        LLM_MODEL_NAME: str
        VL_REC_BACKEND: str
        VL_REC_SERVER_URL: str
        VL_REC_MODEL_NAME: str
        OPENWEBUI_HOST: str
        OPENWEBUI_API_KEY: str

    def __init__(self):
        self.name = "Doc2JSON-Ассистент"
        self.description = "Пайплайн Doc2JSON для OpenWebUI"
        self.config = AppConfig.from_yaml()
        self.llm = None
        self.paddle = None

        self.valves = self.Valves(
            **{
                "pipelines": ["*"],
                "LLM_API_URL": os.getenv("LLM_API_URL", self.config.llm_api_url),
                "LLM_API_KEY": os.getenv("LLM_API_KEY", self.config.llm_api_key),
                "LLM_MODEL_NAME": os.getenv(
                    "LLM_MODEL_NAME", self.config.llm_model_name
                ),
                "VL_REC_BACKEND": os.getenv(
                    "VL_REC_BACKEND", self.config.vl_rec_backend
                ),
                "VL_REC_SERVER_URL": os.getenv(
                    "VL_REC_SERVER_URL", self.config.vl_rec_server_url
                ),
                "VL_REC_MODEL_NAME": os.getenv(
                    "VL_REC_MODEL_NAME", self.config.vl_rec_model_name
                ),
                "OPENWEBUI_HOST": os.getenv(
                    "OPENWEBUI_HOST", self.config.openwebui_host
                ),
                "OPENWEBUI_API_KEY": os.getenv(
                    "OPENWEBUI_API_KEY", self.config.openwebui_token
                ),
            }
        )

    async def on_startup(self):
        logger.info(f"{self.name} starting up...")

        self.paddle = PaddleOCRVL(
            vl_rec_backend=self.valves.VL_REC_BACKEND,
            vl_rec_server_url=self.valves.VL_REC_SERVER_URL,
            vl_rec_model_name=self.valves.VL_REC_MODEL_NAME,
            layout_detection_model_name=self.config.layout_detection_model_name,
            layout_detection_model_dir=self.config.layout_detection_model_dir,
            doc_orientation_classify_model_name=self.config.doc_orientation_classify_model_name,
            doc_orientation_classify_model_dir=self.config.doc_orientation_classify_model_dir,
            use_doc_orientation_classify=self.config.use_doc_orientation_classify,
            use_doc_unwarping=self.config.use_doc_unwarping,
            use_layout_detection=self.config.use_layout_detection,
            layout_threshold=self.config.layout_threshold,
            layout_nms=self.config.layout_nms,
            layout_unclip_ratio=self.config.layout_unclip_ratio,
            layout_merge_bboxes_mode=self.config.layout_merge_bboxes_mode,
        )
        logger.info(f"PaddleOCRVL {self.valves.VL_REC_MODEL_NAME} started")

        self.llm = ChatOpenAI(
            base_url=self.valves.LLM_API_URL,
            api_key=self.valves.LLM_API_KEY,
            model=self.valves.LLM_MODEL_NAME,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            max_tokens=self.config.max_tokens,
            reasoning_effort=self.config.reasoning_effort,
            timeout=self.config.timeout,
        )
        logger.info(f"LLM {self.valves.LLM_MODEL_NAME} started")

    async def on_shutdown(self):
        logger.info(f"{self.name} shutting down...")

    def _fix_json_with_llm(self, broken_json_text: str) -> str:
        """Просит LLM исправить невалидный JSON по format_instructions."""
        system_fix = """
        Ты AI помощник, который исправляет JSON.
        Верни **только валидный JSON**, строго соответствующий Pydantic-схеме.
        {format_instructions}
        """
        user_fix = """
        Исправь этот текст так, чтобы результат был корректным JSON:
        {broken_json_text}
        """
        fix_template = ChatPromptTemplate.from_messages(
            [("system", system_fix), ("user", user_fix)]
        )
        messages = fix_template.format_messages(
            format_instructions=format_instructions,
            broken_json_text=broken_json_text,
        )
        resp = self.llm.invoke(messages)
        return resp.content

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def _call_llm_and_parse(self, messages):
        """Вызов LLM, парсинг в ParsedPDF; при ошибке — попытка починить JSON через LLM и повторить парсинг."""
        result = self.llm.invoke(messages)
        raw_text = result.content

        try:
            return output_parser.parse(raw_text)
        except Exception as e:
            logger.warning("Primary parse failed, attempting JSON repair: %s", e)
            fixed_json = self._fix_json_with_llm(raw_text)
            try:
                return output_parser.parse(fixed_json)
            except Exception as e2:
                logger.exception("JSON repair also failed: %s", e2)
                raise

    async def inlet(self, body: dict, user: dict) -> dict:
        """
        Скачивает PDF из body["files"] во временные файлы и кладёт пути в body["_doc2json_pdf_paths"].
        В pipe файлы не приходят — только то, что подготовлено здесь.
        """
        files = body.get("files", []) or []
        pdf_files = [
            f
            for f in files
            if (f.get("file") or {}).get("meta", {}).get("content_type")
            == "application/pdf"
        ]
        file_list = [
            {
                "url": f["url"],
                "name": f.get("name", "unknown.pdf"),
                "id": f.get("id") or (f.get("file") or {}).get("id"),
            }
            for f in pdf_files
            if f.get("url")
        ]
        body["_doc2json_pdf_paths"] = []
        if file_list:
            try:
                body["_doc2json_pdf_paths"] = await download_pdfs_to_temp_paths(
                    file_list,
                    self.valves.OPENWEBUI_HOST,
                    self.valves.OPENWEBUI_API_KEY,
                )
            except Exception as e:
                logger.exception("Failed to download PDFs in inlet: %s", e)
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        return body

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict,
    ) -> Union[str, dict]:
        """
        Обработка запроса: PDF-пути берутся из body["_doc2json_pdf_paths"] (подготовлены в inlet).
        При отсутствии путей — «Прикрепите файл»; иначе PaddleOCRVL → markdown → LLM → enrich_json.
        """
        logger.info("Starting Doc2JSON pipeline")

        temp_paths = body.get("_doc2json_pdf_paths") or []
        if not temp_paths:
            return "Прикрепите файл."

        all_markdown_list = []
        try:
            for input_path in temp_paths:
                output = self.paddle.predict(input=input_path)
                for res in output:
                    md_info = res.markdown
                    all_markdown_list.append(md_info)

            final_markdown = self.paddle.concatenate_markdown_pages(all_markdown_list)
            markdown_result = html_to_markdown_with_tables(final_markdown)
            markdown_result = truncate_after_diluted_eps(
                remove_parentheses_around_numbers(markdown_result)
            )
        finally:
            for p in temp_paths:
                Path(p).unlink(missing_ok=True)

        messages_for_llm = PROMPT_TEMPLATE.format_messages(
            format_instructions=format_instructions,
            report=markdown_result,
        )

        try:
            parsed = self._call_llm_and_parse(messages_for_llm)
            data = parsed.model_dump(by_alias=True)
            result = enrich_json(data)
            logger.info("Doc2JSON pipeline completed successfully")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.exception("LLM/parse error: %s", e)
            return f"Ошибка при разборе отчёта: {e}"

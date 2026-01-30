import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Union

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

pipelines_dir = os.path.dirname(os.path.abspath(__file__))
if pipelines_dir not in sys.path:
    sys.path.insert(0, pipelines_dir)

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from ocr_utils.config import AppConfig
from ocr_utils.file_utils import download_pdfs_to_temp_paths
from ocr_utils.markdown_utils import html_to_markdown_with_tables
from ocr_utils.models import (
    AccountingStatementsModel,
    OfficialRequestModel,
    RouterResponseModel,
)
from ocr_utils.prompts import (
    ACCOUNTING_STATEMENTS_SYSTEM_PROMPT,
    ACCOUNTING_STATEMENTS_USER_PROMPT,
    FIX_JSON_SYSTEM_PROMPT,
    FIX_JSON_USER_PROMPT,
    OFFICIAL_REQUEST_SYSTEM_PROMPT,
    OFFICIAL_REQUEST_USER_PROMPT,
    ROUTER_SYSTEM_PROMPT,
    ROUTER_USER_PROMPT,
)
from ocr_utils.state import Doc2JSONState
from ocr_utils.text_utils import (
    enrich_json,
    remove_parentheses_around_numbers,
    truncate_after_diluted_eps,
)
from paddleocr import PaddleOCRVL
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed


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
        self.graph = None
        # Кэш URL загруженных файлов по (user_id, chat_id)
        self._file_cache = {}

        self.accounting_output_parser = PydanticOutputParser(
            pydantic_object=AccountingStatementsModel
        )
        self.accounting_format_instructions = (
            self.accounting_output_parser.get_format_instructions()
        )
        self.official_output_parser = PydanticOutputParser(
            pydantic_object=OfficialRequestModel
        )
        self.official_format_instructions = (
            self.official_output_parser.get_format_instructions()
        )
        self.router_output_parser = PydanticOutputParser(
            pydantic_object=RouterResponseModel
        )
        self.router_format_instructions = (
            self.router_output_parser.get_format_instructions()
        )
        self.accounting_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", ACCOUNTING_STATEMENTS_SYSTEM_PROMPT),
                ("user", ACCOUNTING_STATEMENTS_USER_PROMPT),
            ]
        )
        self.fix_prompt_template = ChatPromptTemplate.from_messages(
            [("system", FIX_JSON_SYSTEM_PROMPT), ("user", FIX_JSON_USER_PROMPT)]
        )
        self.official_request_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", OFFICIAL_REQUEST_SYSTEM_PROMPT),
                ("user", OFFICIAL_REQUEST_USER_PROMPT),
            ]
        )
        self.router_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", ROUTER_SYSTEM_PROMPT),
                ("user", ROUTER_USER_PROMPT),
            ]
        )
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
        self._build_graph()
        logger.info("LangGraph router compiled")

    async def on_shutdown(self):
        logger.info(f"{self.name} shutting down...")

    def _fix_json_with_llm(
        self,
        broken_json_text: str,
        format_instructions: str,
    ) -> str:
        """Просит LLM исправить невалидный JSON по format_instructions."""
        messages = self.fix_prompt_template.format_messages(
            broken_json_text=broken_json_text,
            format_instructions=format_instructions,
        )
        resp = self.llm.invoke(messages)
        return resp.content

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def _call_llm_and_parse(self, messages, parser, format_instructions: str):
        """Вызов LLM, парсинг через переданный parser; при ошибке — попытка починить JSON через LLM."""
        result = self.llm.invoke(messages)
        raw_text = result.content

        try:
            return parser.parse(raw_text)
        except Exception as e:
            logger.warning("Primary parse failed, attempting JSON repair: %s", e)
            fixed_json = self._fix_json_with_llm(raw_text, format_instructions)
            try:
                return parser.parse(fixed_json)
            except Exception as e2:
                logger.exception("JSON repair also failed: %s", e2)
                raise

    def _router_node(self, state: Doc2JSONState) -> dict:
        """Узел маршрутизации: LLM определяет категорию документа."""
        messages = self.router_prompt_template.format_messages(
            format_instructions=self.router_format_instructions,
            markdown_text=state["markdown_result"][:30000],
        )
        parsed = self._call_llm_and_parse(
            messages, self.router_output_parser, self.router_format_instructions
        )
        return {"route": parsed.route}

    def _accounting_node(self, state: Doc2JSONState) -> dict:
        """Узел бухгалтерской отчётности: LLM + валидация AccountingStatements → JSON."""
        messages = self.accounting_prompt_template.format_messages(
            format_instructions=self.accounting_format_instructions,
            report=state["markdown_result"],
        )
        parsed = self._call_llm_and_parse(
            messages, self.accounting_output_parser, self.accounting_format_instructions
        )
        data = parsed.model_dump(by_alias=True)
        result = enrich_json(data)
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        return {"response": f"```json\n{json_str}\n```"}

    def _official_request_node(self, state: Doc2JSONState) -> dict:
        """Узел официальных запросов: LLM + валидация OfficialRequest → JSON."""
        messages = self.official_request_prompt_template.format_messages(
            format_instructions=self.official_format_instructions,
            report=state["markdown_result"],
        )
        parsed = self._call_llm_and_parse(
            messages, self.official_output_parser, self.official_format_instructions
        )
        data = parsed.model_dump(by_alias=True)
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return {"response": f"```json\n{json_str}\n```"}

    def _other_node(self, _state: Doc2JSONState) -> dict:
        """Узел «прочее»: документ не относится к бухотчётности и не к официальным запросам."""
        return {
            "response": "Документ не относится к Бухгалтерской отчетности или официальным запросам"
        }

    def _route_after_router(self, state: Doc2JSONState) -> str:
        """Условный переход после роутера: имя следующего узла."""
        next_node = state.get("route") or "other"
        logger.info("Роутер: выбран узел '%s'", next_node)
        return next_node

    def _build_graph(self):
        """Собирает LangGraph: START → router → accounting | official_request | other → END."""
        builder = StateGraph(Doc2JSONState)
        builder.add_node("router", self._router_node)
        builder.add_node("accounting_statements", self._accounting_node)
        builder.add_node("official_request", self._official_request_node)
        builder.add_node("other", self._other_node)
        builder.add_edge(START, "router")
        builder.add_conditional_edges(
            "router",
            self._route_after_router,
            {
                "accounting_statements": "accounting_statements",
                "official_request": "official_request",
                "other": "other",
            },
        )
        builder.add_edge("accounting_statements", END)
        builder.add_edge("official_request", END)
        builder.add_edge("other", END)
        self.graph = builder.compile()

    async def inlet(self, body: dict, user: dict) -> dict:
        """
        Скачивает PDF из body["files"] во временные файлы и кладёт пути в body["_doc2json_pdf_paths"].
        """
        metadata = body.get("metadata", {})
        user_id = metadata.get("user_id")
        chat_id = metadata.get("chat_id")

        if user_id not in self._file_cache:
            self._file_cache[user_id] = {}
        if chat_id not in self._file_cache[user_id]:
            self._file_cache[user_id][chat_id] = set()

        files = body.get("files", []) or []
        pdf_files = [
            f
            for f in files
            if (f.get("file") or {}).get("meta", {}).get("content_type")
            == "application/pdf"
        ]
        file_list_all = [
            {
                "url": f["url"],
                "name": f.get("name", "unknown.pdf"),
                "id": f.get("id") or (f.get("file") or {}).get("id"),
            }
            for f in pdf_files
            if f.get("url")
        ]

        if file_list_all:
            names_all = [f["name"] for f in file_list_all]
            logger.info("Inlet: получены файлы: %s", names_all)

        cached_urls = self._file_cache[user_id][chat_id]
        file_list_new = [f for f in file_list_all if f["url"] not in cached_urls]

        if file_list_new:
            names_new = [f["name"] for f in file_list_new]
            logger.info("Inlet: новые файлы: %s", names_new)
        elif file_list_all:
            logger.info("Inlet: все файлы уже в кэше, новых нет")

        body["_doc2json_pdf_paths"] = []
        body["_doc2json_all_cached"] = bool(file_list_all and not file_list_new)
        if file_list_new:
            try:
                body["_doc2json_pdf_paths"] = await download_pdfs_to_temp_paths(
                    file_list_new,
                    self.valves.OPENWEBUI_HOST,
                    self.valves.OPENWEBUI_API_KEY,
                )
                for f in file_list_new:
                    cached_urls.add(f["url"])
            except Exception as e:
                logger.exception("Failed to download PDFs in inlet: %s", e)
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """Удаляет оставшиеся временные PDF."""
        temp_paths = body.get("_doc2json_pdf_paths") or []
        if temp_paths:
            logger.info(
                "Outlet: очистка временной папки, удаление %d файл(ов): %s",
                len(temp_paths),
                [os.path.basename(p) for p in temp_paths],
            )
        for p in temp_paths:
            Path(p).unlink(missing_ok=True)
        body.pop("_doc2json_pdf_paths", None)
        body.pop("_doc2json_all_cached", None)
        return body

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict,
    ) -> Union[str, dict]:
        """
        Обработка запроса: PDF-пути берутся из body["_doc2json_pdf_paths"] и обрабатываются PaddleOCRVL.
        """
        logger.info("Starting Doc2JSON pipeline")

        temp_paths = body.get("_doc2json_pdf_paths") or []
        if not temp_paths:
            if body.get("_doc2json_all_cached"):
                return "Все прикреплённые файлы уже были обработаны в этом чате ранее. Прикрепите новые PDF для разбора."
            return "Файл не найден. Прикрепите, пожалуйста, pdf файл."

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
            if temp_paths:
                logger.info(
                    "Pipe: очистка временных файлов после обработки (%d шт.): %s",
                    len(temp_paths),
                    [os.path.basename(p) for p in temp_paths],
                )
            for p in temp_paths:
                Path(p).unlink(missing_ok=True)

        if self.graph is None:
            self._build_graph()

        initial_state: Doc2JSONState = {
            "markdown_result": markdown_result,
            "route": None,
            "response": None,
        }
        try:
            final_state = self.graph.invoke(initial_state)
            response = final_state.get("response")
            if response is None:
                return "Документ не относится к Бухгалтерской отчетности или официальным запросам"
            logger.info("Doc2JSON pipeline completed successfully")
            return response
        except Exception as e:
            logger.exception("Pipeline/LLM error: %s", e)
            return f"Ошибка при разборе документа: {e}"

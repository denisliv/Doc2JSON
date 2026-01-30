from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class AppConfig:
    llm_api_url: str
    llm_api_key: str
    llm_model_name: str
    temperature: float
    top_p: float
    max_tokens: int
    reasoning_effort: str
    timeout: int

    vl_rec_backend: str
    vl_rec_server_url: str
    vl_rec_model_name: str
    layout_detection_model_name: str
    layout_detection_model_dir: str
    doc_orientation_classify_model_name: str
    doc_orientation_classify_model_dir: str
    use_doc_orientation_classify: bool
    use_doc_unwarping: bool
    use_layout_detection: bool
    layout_threshold: float
    layout_nms: bool
    layout_unclip_ratio: list[float, float]
    layout_merge_bboxes_mode: str

    openwebui_host: str
    openwebui_token: str

    @classmethod
    def from_yaml(cls, path: str = "pipelines/ocr_utils/config.yaml") -> "AppConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(
            llm_api_url=data["llm_api_url"],
            llm_api_key=data["llm_api_key"],
            llm_model_name=data["llm_model_name"],
            temperature=data["temperature"],
            top_p=data["top_p"],
            max_tokens=data["max_tokens"],
            reasoning_effort=data["reasoning_effort"],
            timeout=data["timeout"],
            vl_rec_backend=data["vl_rec_backend"],
            vl_rec_server_url=data["vl_rec_server_url"],
            vl_rec_model_name=data["vl_rec_model_name"],
            layout_detection_model_name=data["layout_detection_model_name"],
            layout_detection_model_dir=data["layout_detection_model_dir"],
            doc_orientation_classify_model_name=data[
                "doc_orientation_classify_model_name"
            ],
            doc_orientation_classify_model_dir=data[
                "doc_orientation_classify_model_dir"
            ],
            use_doc_orientation_classify=data["use_doc_orientation_classify"],
            use_doc_unwarping=data["use_doc_unwarping"],
            use_layout_detection=data["use_layout_detection"],
            layout_threshold=data["layout_threshold"],
            layout_nms=data["layout_nms"],
            layout_unclip_ratio=data["layout_unclip_ratio"],
            layout_merge_bboxes_mode=data["layout_merge_bboxes_mode"],
            openwebui_host=data["openwebui_host"],
            openwebui_token=data["openwebui_token"],
        )

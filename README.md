## Doc2JSON — OCR-пайплайн PDF → JSON для OpenWebUI

Doc2JSON — это пайплайн для OpenWebUI, который принимает PDF‑файлы, распознаёт их содержимое с помощью `PaddleOCR-VL`, конвертирует в markdown, а затем с помощью LLM извлекает структурированные данные в формате JSON.

### Структура проекта

```
Doc2JSON/
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
├── fix_paddlex_imports.sh
└── pipelines/
    ├── pipeline.py              # основной пайплайн (inlet → pipe → outlet, LangGraph)
    ├── PP-DocLayoutV2/          # модель детекции разметки страницы (PaddleOCR)
    ├── PP-LCNet_x1_0_doc_ori/   # модель классификации ориентации документа
    └── ocr_utils/
        ├── config.py            # загрузка конфигурации из YAML
        ├── config.yaml          # настройки LLM, OCR, OpenWebUI
        ├── state.py             # состояние графа (Doc2JSONState)
        ├── file_utils.py        # скачивание PDF по URL
        ├── markdown_utils.py    # конвертация HTML → markdown с таблицами
        ├── text_utils.py        # постобработка текста (enrich_json, truncate и др.)
        ├── models/              # Pydantic-модели для парсинга ответов LLM
        │   ├── __init__.py
        │   ├── router.py        # RouterResponseModel (категория документа)
        │   ├── accounting_statements.py  # баланс + отчёт о прибылях и убытках
        │   └── official_request.py       # официальные запросы (ФЛ/ЮЛ, счета, карты и т.д.)
        └── prompts/             # системные и пользовательские промпты для LLM
            ├── __init__.py
            ├── router.py        # роутер
            ├── accounting_statements.py  # баланс + отчёт о прибылях и убытках
            ├── official_request.py       # официальные запросы (ФЛ/ЮЛ, счета, карты и т.д.)
            └── fix_json.py      # починка невалидного JSON
```

### Общая схема работы

- **Вход в пайплайн (`inlet`)**
  - Из `body["files"]` берутся вложения с типом `application/pdf`.
  - Для каждого PDF формируется список `{url, name, id}`.
  - По `(user_id, chat_id)` ведётся кэш уже обработанных URL, чтобы не скачивать один и тот же файл несколько раз.
  - Новые файлы скачиваются во временные пути функцией `download_pdfs_to_temp_paths`, пути сохраняются в `body["_doc2json_pdf_paths"]`.

- **Основная обработка (`pipe`)**
  - Если `_doc2json_pdf_paths` пустой, пользователю возвращается сообщение: нужно прикрепить PDF.
  - Иначе вызывается `_process_files_with_paddleocr(temp_paths)`:
    - поднимается `PaddleOCRVL` с параметрами из `AppConfig`/переменных окружения;
    - для каждого PDF вызывается `ocr.predict`, из результатов берётся поле `markdown`;
    - все страницы объединяются в один markdown (`concatenate_markdown_pages`);
    - HTML‑разметка конвертируется в markdown с таблицами (`html_to_markdown_with_tables`);
    - выполняется пост‑обработка текста (`remove_parentheses_around_numbers`, `truncate_after_diluted_eps`).
  - Получившийся `markdown_result` передаётся в граф состояний (`LangGraph`), который решает, как именно парсить документ.

- **Маршрутизация документов (router‑узел)**
  - Узел `_router_node` формирует промпт `ROUTER_SYSTEM_PROMPT` + `ROUTER_USER_PROMPT` и передаёт в LLM первые ~30000 символов markdown.
  - Ответ парсится в модель `RouterResponseModel(route=...)` через `_call_llm_and_parse`.
  - Поддерживаемые маршруты:
    - `accounting_statements` — формы бухгалтерской отчётности;
    - `official_request` — официальные запросы госорганов/аудиторов/и т.п.;
    - `other` — всё остальное.
  - В зависимости от `route` граф ведёт выполнение в один из узлов: `accounting_statements`, `official_request` или `other`.

- **Ветка бухгалтерской отчётности (`_accounting_node`)**
  - Формируется промпт `ACCOUNTING_STATEMENTS_SYSTEM_PROMPT` + `ACCOUNTING_STATEMENTS_USER_PROMPT`.
  - LLM возвращает JSON, который приводится к модели `AccountingStatementsModel`:
    - таблицы баланса (активы/пассивы, разделы I–V, коды строк 110, 120, 300, 700 и т.д.);
    - отчёт о прибылях и убытках (выручка, расходы, налоги, чистая и совокупная прибыль и т.п.).
  - Полученный pydantic‑объект сериализуется в dict с alias‑полями, затем обогащается функцией `enrich_json`.
  - Результат возвращается в виде ```json‑блока.

- **Ветка официальных запросов (`_official_request_node`)**
  - Формируется промпт `OFFICIAL_REQUEST_SYSTEM_PROMPT` + `OFFICIAL_REQUEST_USER_PROMPT`.
  - LLM возвращает JSON, который приводится к модели `OfficialRequestModel`, включающей:
    - общие данные запроса (отправитель, номер и дата, тема, срок ответа, период);
    - списки физических и юридических лиц (`Fizik`, `Urik`);
    - информацию о счётах, транзакциях, картах, кредитах, гарантиях, депозитах, АИС ИДО, арестах/ограничениях, СДБО;
    - прочие сущности (ценные бумаги, ЭРИП, доверенности, суд, др.).
  - Полученный pydantic‑объект сериализуется в dict с alias‑полями.
  - Результат возвращается в виде ```json‑блока.

- **Ветка `other`**
  - Если роутер определил, что документ не относится к бухотчётности и не является официальным запросом, возвращается простое текстовое сообщение:
    - _«Документ не относится к Бухгалтерской отчетности или официальным запросам»_.

- **Исправление невалидного JSON**
  - Вызовы LLM для роутера и веток используют общий метод `_call_llm_and_parse`:
    - сначала пытается распарсить ответ сразу в нужную pydantic‑модель;
    - при ошибке включает вспомогательный цикл `_fix_json_with_llm` с промптом `FIX_JSON_SYSTEM_PROMPT`/`FIX_JSON_USER_PROMPT`:
      - в LLM отправляются исходный текст, формат‑инструкции (`parser.get_format_instructions()`) и текст ошибки;
      - из ответа удаляются обрамляющие ```json/``` маркеры;
      - до `max_attempts` раз (по умолчанию 3) выполняются попытки починки.
  - Если после всех попыток JSON так и не проходит валидацию, ошибка логируется, и исключение пробрасывается наружу.

- **Завершение пайплайна (`outlet`)**
  - В `outlet` из `body["_doc2json_pdf_paths"]` удаляются временные PDF‑файлы и очищается ключ из `body`.
  - Это предотвращает накопление файлов на диске между запросами.

### Конфигурация и окружение

- **Конфиг LLM и OCR (`AppConfig`)**
  - Конфигурация читается из `pipelines/ocr_utils/config.yaml` классом `AppConfig` и включает:
    - параметры LLM: `llm_api_url`, `llm_api_key`, `llm_model_name`, `temperature`, `top_p`, `max_tokens`, `reasoning_effort`, `timeout`;
    - параметры `PaddleOCRVL`: `vl_rec_backend`, `vl_rec_server_url`, `vl_rec_model_name` и настройки моделей разметки страницы/ориентации;
    - настройки OpenWebUI‑интеграции: `openwebui_host`, `openwebui_token`.
  - Любой из этих параметров может быть переопределён через Valves:
    - `LLM_API_URL`, `LLM_API_KEY`, `LLM_MODEL_NAME`;
    - `VL_REC_BACKEND`, `VL_REC_SERVER_URL`, `VL_REC_MODEL_NAME`;
    - `OPENWEBUI_HOST`, `OPENWEBUI_API_KEY`.

### Жизненный цикл пайплайна в OpenWebUI

- **Инициализация (`on_startup`)**
  - Создаётся клиент `ChatOpenAI` с параметрами из `valves`/`AppConfig`.
  - Собирается граф состояний `LangGraph` с узлами `router`, `accounting_statements`, `official_request`, `other`.

- **Завершение (`on_shutdown`)**
  - Очищается кэш файлов и ссылки на LLM/граф, вызывается `gc.collect()`.

### Как использовать

- **В OpenWebUI**
  - Подключите пайплайн `Doc2JSON-Ассистент` согласно стандартной схеме интеграции пайплайнов в OpenWebUI.
  - Убедитесь, что:
    - заполнен `pipelines/ocr_utils/config.yaml`;
    - настроены valves для доступа к LLM и OCR‑backend;
  - В чате с ассистентом прикрепите один или несколько PDF‑файлов:
    - пайплайн скачает новые файлы, преобразует в markdown и вернёт:
      - структурированный JSON по бухотчётности;
      - структурированный JSON по официальному запросу;
      - либо текстовое сообщение, что документ не распознан как поддерживаемый тип.


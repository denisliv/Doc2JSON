import json
import re

REQUIRED_TABLES_KEYS = [
    "balance_head_table",
    "balance_dates_table",
    "balance_main_table_dates",
    "balance_main_table",
    "report_main_table",
]


def enrich_json(input_json_str):
    """Добавляет к ответу LLM поля message (OK/Missing по ключам)

    Args:
        text: Исходный JSON
    Returns:
        Исходный JSON c ключами message, xlsx.
    """
    if isinstance(input_json_str, str):
        data = json.loads(input_json_str)
    else:
        data = input_json_str.copy()

    tables_data = data.get("tables_data", {})
    message = {key: "OK" if key in tables_data else "Missing" for key in REQUIRED_TABLES_KEYS}

    return {"message": message, "xlsx": None, **data}


def remove_parentheses_around_numbers(text: str) -> str:
    """
    Убирает скобки вокруг чисел.

    Args:
        text: Исходная строка

    Returns:
        Строка без скобок вокруг числовых выражений.
    """
    if not isinstance(text, str):
        return text

    def replace_match(m):
        inner = m.group(1)
        if re.fullmatch(r"[\d\s]+", inner.strip()):
            return inner
        return m.group(0)

    return re.sub(r"\(([^)]+)\)", replace_match, text)


def truncate_after_diluted_eps(markdown: str) -> str:
    """
    Обрезки markdown после строки «Разводненная прибыль (убыток) на акцию | 260 |».
    Необходимо, если исходный pdf содержит больше таблиц, чем нужно для отчета

    Args:
        markdown: Исходная строка в формате Markdown

    Returns:
        Обрезанная строка или исходная, если шаблон не найден
    """
    lines = markdown.splitlines(keepends=True)
    pattern = "| Разводненная прибыль (убыток) на акцию | 260 |"

    for i, line in enumerate(lines):
        if line.strip().startswith(pattern):
            return "".join(lines[: i + 1])

    return markdown

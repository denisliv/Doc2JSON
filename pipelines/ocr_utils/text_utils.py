import re


def remove_parentheses_around_numbers(text: str) -> str:
    """Убирает скобки вокруг чисел (например, отрицательные в бухгалтерии)."""
    if not isinstance(text, str):
        return text

    def replace_match(m):
        inner = m.group(1)
        if re.fullmatch(r"[\d\s]+", inner.strip()):
            return inner
        return m.group(0)

    return re.sub(r"\(([^)]+)\)", replace_match, text)


def truncate_after_diluted_eps(markdown: str) -> str:
    """Обрезает markdown после строки «Разводненная прибыль (убыток) на акцию | 260 |»."""
    lines = markdown.splitlines(keepends=True)
    pattern = "| Разводненная прибыль (убыток) на акцию | 260 |"

    for i, line in enumerate(lines):
        if line.strip().startswith(pattern):
            return "".join(lines[: i + 1])

    return markdown

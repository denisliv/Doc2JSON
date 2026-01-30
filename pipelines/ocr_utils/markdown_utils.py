from bs4 import BeautifulSoup


def simple_html_table_to_markdown(table) -> str:
    """
    Преобразует HTML-таблицу (BeautifulSoup Tag) в Markdown.

    Args:
        table: Элемент BeautifulSoup (Tag) с таблицей

    Returns:
        Строка таблицы в формате Markdown
    """
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row = [cell.get_text(strip=True).replace("\n", " ") for cell in cells]
        rows.append(row)

    if not rows:
        return ""

    max_cols = max(len(row) for row in rows)
    for row in rows:
        while len(row) < max_cols:
            row.append("")

    lines = []
    for i, row in enumerate(rows):
        line = "| " + " | ".join(row) + " |"
        lines.append(line)
        if i == 0:
            separator = "| " + " | ".join(["---"] * max_cols) + " |"
            lines.append(separator)
    return "\n".join(lines)


def html_to_markdown_with_tables(html: str) -> str:
    """
    Преобразует HTML-строку в Markdown: таблицы — в markdown-таблицы, остальное — в текст.

    Args:
        html: Исходная HTML-строка

    Returns:
        Строка в формате Markdown
    """
    soup = BeautifulSoup(html, "html.parser")
    output = []

    for element in soup.children:
        if element.name == "table":
            md_table = simple_html_table_to_markdown(element)
            output.append(md_table)
            output.append("")
        else:
            text = element.get_text(strip=True)
            if text:
                output.append(text)
                output.append("")

    return "\n".join(output)

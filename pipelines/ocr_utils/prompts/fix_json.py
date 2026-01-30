"""
Промпты для исправления невалидного JSON по Pydantic-схеме.
"""

FIX_JSON_SYSTEM_PROMPT = """
Ты AI помощник, который исправляет JSON.
Верни **валидный JSON**, строго соответствующий этой Pydantic-схеме.
{format_instructions}
"""

FIX_JSON_USER_PROMPT = """
Исправь этот текст так, чтобы результат был корректным JSON:
{broken_json_text}
"""

#!/bin/bash
set -e

FILE=$(find /usr/local/lib/python3.*/site-packages -name "base.py" -path "*/paddlex/inference/pipelines/components/retriever/*" 2>/dev/null | head -n1)

if [ -z "$FILE" ]; then
    echo "Файл base.py не найден. Проверьте установку paddlex."
    exit 1
fi

echo "Патчим: $FILE"
sed -i 's/from langchain\.docstore\.document import Document/from langchain_core.documents import Document/g' "$FILE"
sed -i 's/from langchain\.text_splitter import RecursiveCharacterTextSplitter/from langchain_text_splitters import RecursiveCharacterTextSplitter/g' "$FILE"
echo "Импорты LangChain успешно обновлены"
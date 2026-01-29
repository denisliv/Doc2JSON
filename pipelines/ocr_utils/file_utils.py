import logging
import tempfile
from pathlib import Path

import aiohttp

logger = logging.getLogger(__name__)


async def download_file(url: str, headers: dict) -> bytes:
    """
    Асинхронно загружает файл по указанному URL.

    Args:
        url: URL файла для загрузки
        headers: Словарь с HTTP заголовками, включая авторизацию

    Returns:
        Байты загруженного файла

    Raises:
        Exception: Если HTTP статус ответа не равен 200 или произошла ошибка при загрузке
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                content = await resp.read()
                logger.info(f"Downloaded file: {len(content)} bytes")
                return content
            else:
                error_text = await resp.text()
                raise Exception(
                    f"Failed to download file: HTTP {resp.status} – {error_text}"
                )


async def download_pdf_to_temp_path(
    url: str,
    headers: dict,
    filename_hint: str = "document.pdf",
) -> str:
    """
    Загружает PDF по URL и сохраняет во временный файл.
    Возвращает путь к временному файлу (для передачи в PaddleOCRVL.predict).
    """
    content = await download_file(url, headers)
    suffix = Path(filename_hint).suffix or ".pdf"
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with open(fd, "wb") as f:
            f.write(content)
        return path
    except Exception:
        Path(path).unlink(missing_ok=True)
        raise


async def download_pdfs_to_temp_paths(
    file_list: list[dict],
    openwebui_host: str,
    openwebui_token: str,
) -> list[str]:
    """
    Загружает список PDF-файлов по URL OpenWebUI и сохраняет во временные файлы.
    Возвращает список путей к временным файлам (в том же порядке).
    """
    if not openwebui_token:
        logger.warning("OPENWEBUI_API_KEY not set — skipping file download")
        return []

    headers = {"Authorization": f"Bearer {openwebui_token}"}
    paths = []

    for file_meta in file_list:
        url = f"{openwebui_host.rstrip('/')}{file_meta['url']}/content"
        name = file_meta.get("name", "unknown.pdf")
        try:
            path = await download_pdf_to_temp_path(url, headers, name)
            paths.append(path)
            logger.info(f"Downloaded {name} to temp file")
        except Exception as e:
            logger.error(f"Failed to download {name}: {e}")
            for p in paths:
                Path(p).unlink(missing_ok=True)
            raise

    return paths

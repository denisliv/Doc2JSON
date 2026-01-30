FROM ghcr.io/open-webui/pipelines:main

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ccache && \
    rm -rf /var/lib/apt/lists/*
	
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY pipelines /app/pipelines/

COPY fix_paddlex_imports.sh /tmp/
RUN chmod +x /tmp/fix_paddlex_imports.sh && \
    /tmp/fix_paddlex_imports.sh && \
    rm /tmp/fix_paddlex_imports.sh
	
ENV PYTHONPATH=/app/pipelines
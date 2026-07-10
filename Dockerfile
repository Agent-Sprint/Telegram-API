# syntax=docker/dockerfile:1

FROM python:3.11-slim

ARG WHISPER_MODEL=base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Create uploads directory for file sending feature
RUN mkdir -p /app/uploads

# Install system dependencies required by openai-whisper
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

# Install dependencies first so the layer can be cached when code changes.
COPY requirements.txt .
# Install CPU-only torch first so pip does not pull the CUDA wheel when resolving openai-whisper deps.
# Two separate RUN steps are required: the first commits the CPU torch layer so the second pip
# invocation sees it as already-satisfied and skips re-resolving from PyPI.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the Whisper model at build time so it is baked into the image.
# This eliminates the runtime download on first voice message.
RUN python -c "import whisper; whisper.load_model('${WHISPER_MODEL}')"

# Copy the application code.
COPY . .

# Run as a non-root user for security.
RUN useradd -m appuser \
    && chown -R appuser:appuser /app \
    && chmod -R 755 /app/uploads \
    && chown -R appuser:appuser /root/.cache/whisper
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ============ STAGE 1: Base with Ollama ============
FROM ubuntu:24.04 AS base

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=http://127.0.0.1:11434
ENV GEN_MODEL=gemma3:270m
ENV EMB_MODEL=nomic-embed-text

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# ============ STAGE 2: Install Ollama ============
FROM base AS ollama

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in background and pull models
RUN ollama serve & \
    until curl -s http://localhost:11434/api/tags > /dev/null; do sleep 1; done && \
    ollama pull nomic-embed-text && \
    ollama pull gemma3:270m && \
    pkill ollama

# ============ STAGE 3: Python App ============
FROM ollama AS app

# Copy project files
COPY requirements.txt .
COPY src ./src
COPY .env.example .env
COPY data ./data

# Create virtual environment and install Python deps
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# ============ STAGE 4: Final Runtime ============
FROM app AS final

# Use virtual environment
ENV PATH="/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default: Run FastAPI server
CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
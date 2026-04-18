# Personal Assistant Agent — production image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install minimal system deps used at runtime (curl for healthcheck).
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Install the package itself.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

# Ship the default demo config; override via bind mount or
# PERSONAL_ASSISTANT_AGENT_CONFIG for production.
COPY config.yaml ./config.yaml

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "personal_assistant_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]


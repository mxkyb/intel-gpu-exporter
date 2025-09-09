FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

LABEL org.opencontainers.image.title="intel-gpu-exporter"
LABEL org.opencontainers.image.authors="Bruce Schultz <bschultz013@gmail.com>"
LABEL org.opencontainers.image.source="https://github.com/brucetony/intel-gpu-exporter"

ENV \
    DEBCONF_NONINTERACTIVE_SEEN="true" \
    DEBIAN_FRONTEND="noninteractive" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    REFRESH_PERIOD_MS=10000 \
    DEVICE="" \
    IS_DOCKER=True

RUN apt-get update && apt-get install --no-install-recommends -y intel-gpu-tools 

WORKDIR /app
COPY . .

RUN uv sync --locked

CMD ["uv", "run", "/app/intel-gpu-exporter.py"]

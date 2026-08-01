FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests
COPY dbt ./dbt
COPY dbt_project.yml ./

RUN python -m pip install --upgrade pip \
    && python -m pip install -e ".[dev]"

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "bike_share_etl.check_database_connection"]

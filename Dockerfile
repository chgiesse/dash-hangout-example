FROM python:3.12-slim-bookworm AS builder

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
COPY ./assets /app/assets

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

FROM python:3.12-slim-bookworm AS production
WORKDIR /app
# Create nonroot user first
RUN groupadd -r nonroot && \
    useradd -r -g nonroot nonroot

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /app
RUN chown -R nonroot:nonroot /app
USER nonroot

ENTRYPOINT ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8050", "--workers", "2", "--proxy-headers", "--timeout-keep-alive", "240", "--log-level", "error", "app:server"]            
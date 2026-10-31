
# Stage 1: Install dependencies
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

COPY requirements-runtime.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements-runtime.txt && \
    pip install --no-cache-dir --prefix=/install --upgrade setuptools wheel

# Stage 2: Run the API
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src ./src
COPY model.joblib .
RUN pip uninstall -y setuptools wheel

# Run as non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

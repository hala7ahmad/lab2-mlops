
# AI381 Lab 2 – MLOps Churn Prediction API

[![CI](https://github.com/hala7ahmad/lab2-mlops/actions/workflows/ci.yml/badge.svg)](https://github.com/hala7ahmad/lab2-mlops/actions/workflows/ci.yml)

## Project Overview

This project demonstrates an MLOps workflow for a customer churn prediction model.

The trained machine learning model is served through a FastAPI application, packaged in Docker, tested using Pytest, and deployed to GitHub Container Registry (GHCR) through GitHub Actions.

## Technologies

- Python 3.11
- FastAPI and Pydantic
- Scikit-learn and Joblib
- Pytest
- Docker
- GitHub Actions
- Trivy
- GitHub Container Registry (GHCR)

## Quick Start – One Command

With Docker Desktop running, start the published API using:

```bash
docker run --rm -p 8000:8000 ghcr.io/hala7ahmad/lab2-mlops:5c35d9fd7b2eba298a5c41e56b5521d273377a80
```

If the GHCR package is private, authenticate to GHCR first.

## Build and Run Locally

Build the Docker image:

```bash
docker build -t churn-api .
```

Start the container:

```bash
docker run --rm -p 8000:8000 churn-api
```

## API Endpoints

### Health Check

GET `/health`

URL: http://localhost:8000/health

Expected response:

```json
{"status": "ok"}
```

### Prediction

POST `/predict`

The endpoint accepts validated customer information and returns a churn probability.

Interactive API documentation:

http://localhost:8000/docs

Example prediction request from the project directory:

```powershell
curl.exe -X POST http://localhost:8000/predict -H "Content-Type: application/json" --data-binary "@sample_request.json"
```

## Run Tests

Install the development dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest -q
```

The test suite includes five checks:

1. Health endpoint response
2. Model loading
3. Input validation
4. Edge case handling
5. Deterministic prediction

## Docker Configuration

The application uses a multi-stage Dockerfile to separate dependency installation from runtime.

The container runs under a non-root user and includes a HEALTHCHECK.

Runtime dependencies are maintained separately in `requirements-runtime.txt`.

## CI/CD Pipeline

GitHub Actions performs the following:

- Runs tests on pull requests and pushes.
- Builds the Docker image on the main branch.
- Scans the image using Trivy.
- Pushes the image to GHCR with a commit SHA tag.

The Trivy quality gate blocks HIGH and CRITICAL vulnerabilities when a fix is available. Vulnerabilities without available fixes are excluded using `--ignore-unfixed`, but they may still exist in the image.

## Branch Protection

The `main` branch requires a pull request and a successful `test` status check before merging.

## Container Registry

Published image:

`ghcr.io/hala7ahmad/lab2-mlops`

Image digest:

`sha256:e79d2e7262d323d405c27b864667c00b9ee7ac9cdda1a0119181b172df969786`

## Repository

https://github.com/hala7ahmad/lab2-mlops

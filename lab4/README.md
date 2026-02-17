# Lab 4: Summarization Backend API

FastAPI-based text summarization service with OpenRouter integration and JWT-style authentication.

## Setup

### 1. Create and activate virtual environment

```bash
cd lab4
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install .              # Production dependencies
pip install ".[dev]"       # Including pytest for tests
```

### 3. Configure environment

Copy `env.example` to `.env` and add your OpenRouter API key:

```bash
cp env.example .env
# Edit .env and replace your_api_key_here with your actual key
```

## Run the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Test the API

### Health check (no auth required)

```bash
curl http://localhost:8000/health
```

### Summarize (auth required)

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-token" \
  -d '{"text": "Your text to summarize here.", "max_length": 50}'
```

### Failure cases to verify

- Missing token: omit `-H "Authorization: Bearer dev-token"` → expect HTTP 401
- Invalid token: use `-H "Authorization: Bearer wrong-token"` → expect HTTP 401
- Empty text: `"text": ""` → expect HTTP 422

## Run tests

```bash
pytest
# or
python -m pytest
```

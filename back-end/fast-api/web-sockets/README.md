# ⚡ Fast API - Web Sockets

## Environment

```bash
pyenv local 3.10.0

python -m venv .venv \
  && source .venv/bin/activate \
  && python -m pip install --upgrade pip \
  && pip install "fastapi==0.72.0"
```

## Application

```bash
uvicorn main:app --reload
```

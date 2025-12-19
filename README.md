# reality-telegram-bot

Run:
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- mkdir -p data
- cp .env.example .env (or create .env)
- uvicorn app.main:app --reload

Endpoints:
- GET /health

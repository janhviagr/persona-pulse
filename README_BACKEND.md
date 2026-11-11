# Backend (Person 2) quick start - Windows Command Prompt

    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r backend\requirements.txt
    copy .env.example .env
    py -m uvicorn backend.app.main:app --reload --port 8000

Docs: http://localhost:8000/docs
Tests:  py -m pytest backend\tests
Regenerate contracts:  py -m scripts.export_contracts

Run all commands from the repo root (persona-pulse/) so `backend` and `ai_engine` are importable.

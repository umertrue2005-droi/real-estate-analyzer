# Autonomous Real Estate Investment Analyzer

A full-stack property investment analyzer with a Next.js 14 frontend, FastAPI backend, SQLAlchemy/PostgreSQL persistence, Celery/Redis task orchestration, JWT auth, and mock-first integrations for ATTOM, Rentcast, Walk Score, Census, and GPT-4o synthesis.

The app is designed to work even with zero API keys. Every external service tries the real API when a key is present and returns realistic mock data if the key is missing or the call fails.

## Run With Docker

```bash
cp .env.example .env
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

Frontend: http://localhost:3000  
Backend API: http://localhost:8000  
API docs: http://localhost:8000/docs

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Notes

- No Zillow API and no Clerk are used.
- Auth is email/password with JWT tokens stored in `localStorage`.
- In Docker, Celery processes the agent pipeline. If Celery/Redis is unavailable during direct backend development, the API falls back to FastAPI background tasks.
- The default local backend also falls back to SQLite when a PostgreSQL driver/database is unavailable, while Docker uses PostgreSQL.


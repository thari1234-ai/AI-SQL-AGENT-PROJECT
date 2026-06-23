# AI SQL Agent

**Chat with Your Database.**

AI SQL Agent is a production-style SaaS starter platform that lets users connect to a PostgreSQL database, ask questions in natural language, generate secure SQL, run analytics, and visualize results.

## Stack
- Frontend: Next.js 15, TypeScript, Tailwind CSS, React Query, ECharts
- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic-ready structure
- Database: PostgreSQL
- Auth: JWT

## Features Implemented
- Beautiful landing page and dashboard shell
- JWT signup/login and protected API routes
- Natural-language prompt -> SQL generation service (mock-ready for real LLM)
- SQL safety layer (read-only SELECT, keyword blocking, timeout, row limits)
- Result table and automatic chart detection
- Business insight generation scaffold
- Query history with CSV/XLSX export
- Data explorer endpoints for schema introspection
- Dashboard and widget APIs
- Rate limiting and audit logs
- Dockerized local environment

## Project Structure
- `frontend/` Next.js app
- `backend/` FastAPI app
- `docs/` architecture and API docs
- `docker-compose.yml` full local stack

## Quick Start (Docker)
1. Copy env files:
   - `backend/.env.example` -> `backend/.env`
   - `frontend/.env.example` -> `frontend/.env.local`
2. Run:
   - `docker compose up --build`
3. Open:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs

## Quick Start (Local Dev)
### Backend
1. `cd backend`
2. `python -m venv .venv`
3. `.venv\\Scripts\\Activate.ps1`
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Kaggle Dataset Bootstrapping
1. Create tables in PostgreSQL (example: `sales`)
2. Import CSV into PostgreSQL with `COPY`
3. Validate table availability in Data Explorer

## Automatic Demo Data (Handled)
- On backend startup, the app automatically creates a `sales` table (if missing) and inserts demo rows when table is empty.
- This behavior is controlled by `AUTO_SEED_DEMO_DATA=true` in backend environment.
- You can switch it off in production by setting `AUTO_SEED_DEMO_DATA=false`.

## Production Notes
- Replace mock LLM service in `backend/app/services/llm_service.py` with provider SDK calls.
- Add refresh tokens, RBAC, and tenant-aware schemas.
- Add Redis-backed rate limiting and cache.
- Add Alembic migrations and CI pipelines.

## Free Deployment
- End-to-end free-tier deployment guide: `docs/free-deployment.md`
- Render blueprint file: `render.yaml`

## Google Free Tier LLM Setup
1. Get a Gemini API key from Google AI Studio.
2. In `backend/.env` set:
   - `LLM_PROVIDER=google`
   - `LLM_API_KEY=your_key_here`
   - Optional: `LLM_MODEL=gemini-2.0-flash`
3. Restart backend.

If key/model is missing or provider fails, the app safely falls back to mock SQL generation.

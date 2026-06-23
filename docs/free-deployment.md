# Free Deployment Runbook

## Recommended Stack
- Frontend: Vercel Hobby
- Backend: Render Free Web Service
- Database: Neon PostgreSQL Free Tier

## 1) Neon
- Create project and database.
- Copy host, port, database, user, password.

## 2) Render (Backend)
- Create new Blueprint and point to repo root (`render.yaml`).
- Set secret env vars in Render dashboard:
  - `SECRET_KEY`
  - `LLM_API_KEY`
  - `POSTGRES_HOST`
  - `POSTGRES_PORT`
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`
  - `POSTGRES_DB`
  - `CORS_ORIGINS` (any of these formats work):
    - `https://your-vercel-domain.vercel.app`
    - `https://your-vercel-domain.vercel.app,https://www.your-domain.com`
    - `["https://your-vercel-domain.vercel.app"]`
  - Optional: `AUTO_SEED_DEMO_DATA=false` (disable demo table seeding in production)
- Deploy and verify `GET /health`.

## 3) Vercel (Frontend)
- Import GitHub repo.
- Set Root Directory to `frontend`.
- Add env var `NEXT_PUBLIC_API_URL` = `https://your-render-service.onrender.com/api/v1`.
- Deploy.

## 3.1) Backend CORS After Frontend Deploy
- After Vercel gives your final domain, update Render env var:
  - `CORS_ORIGINS=https://your-final-vercel-domain.vercel.app`
- Redeploy backend.

## 4) Post-Deploy Checks
- Signup/login flow works.
- Chat request returns SQL and explanation.
- History loads.
- Explorer lists tables.

## Notes
- Render free instances can sleep and cold-start.
- Gemini free tier may throttle or block until quota is enabled.
- If signup fails, verify backend `/health`, `NEXT_PUBLIC_API_URL`, and CORS value first.

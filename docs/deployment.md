# Deployment Instructions

## Option A: Docker Compose
```bash
docker compose up --build -d
```

## Option B: Split Deploy
- Deploy frontend (`frontend/`) to Vercel.
- Deploy backend (`backend/`) to Azure Container Apps, AWS ECS, or Render.
- Use managed PostgreSQL (Azure Database for PostgreSQL / RDS).

## Environment Variables
### Frontend
- `NEXT_PUBLIC_API_URL`

### Backend
- `SECRET_KEY`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `LLM_PROVIDER`
- `LLM_API_KEY`

## Hardening Checklist
- Enforce HTTPS
- Rotate JWT secret
- Add Redis rate limiter
- Enable structured centralized logging
- Add observability (OpenTelemetry)

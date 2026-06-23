from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as api_router
from app.core.config import settings
from app.db.session import SessionLocal, init_db
from app.services.bootstrap.data_seed import ensure_sales_seed_data


app = FastAPI(
    title="AI SQL Agent API",
    version="1.0.0",
    description="Enterprise-ready API for natural language analytics over SQL databases.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    if settings.auto_seed_demo_data:
        db = SessionLocal()
        try:
            ensure_sales_seed_data(db)
        finally:
            db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")

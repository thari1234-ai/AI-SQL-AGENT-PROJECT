from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.api.v1.dashboards import router as dashboards_router
from app.api.v1.explorer import router as explorer_router
from app.api.v1.history import router as history_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(chat_router)
router.include_router(history_router)
router.include_router(explorer_router)
router.include_router(dashboards_router)

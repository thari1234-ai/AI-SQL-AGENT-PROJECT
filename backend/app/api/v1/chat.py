from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, rate_limit
from app.db.session import get_db
from app.models import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

router = APIRouter(prefix="/chat", tags=["chat"], dependencies=[Depends(rate_limit)])


@router.post("", response_model=ChatResponse)
def chat_endpoint(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ChatResponse:
    return process_chat(payload.prompt, db, user)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, rate_limit
from app.db.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserResponse
from app.services.auth_service import login, signup

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(rate_limit)])


@router.post("/signup", response_model=TokenResponse)
def signup_endpoint(payload: SignupRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return signup(payload, db)


@router.post("/login", response_model=TokenResponse)
def login_endpoint(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return login(payload, db)


@router.get("/me", response_model=UserResponse)
def me_endpoint(user: User = Depends(get_current_user)) -> UserResponse:
    return user

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import AuditLog, User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse


def signup(payload: SignupRequest, db: Session) -> TokenResponse:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.flush()
    db.add(AuditLog(user_id=user.id, action="signup", details={"email": user.email}))
    db.commit()

    return TokenResponse(access_token=create_access_token(user.email))


def login(payload: LoginRequest, db: Session) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    db.add(AuditLog(user_id=user.id, action="login", details={}))
    db.commit()
    return TokenResponse(access_token=create_access_token(user.email))

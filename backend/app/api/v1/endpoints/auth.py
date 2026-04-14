from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_active_user, get_db
from app.core.rate_limit import enforce_login_rate_limit
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email_exists = db.query(User).filter(User.email == payload.email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    username_exists = db.query(User).filter(User.username == payload.username).first()
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse, summary="Login and receive access token")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    identifier = request.client.host if request.client else payload.email
    enforce_login_rate_limit(identifier)

    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return TokenResponse(access_token=token, user_id=user.id, role=user.role)


@router.get("/me", response_model=UserResponse, summary="Get current authenticated user")
def me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/refresh", response_model=TokenResponse, summary="Refresh access token")
def refresh(current_user: User = Depends(get_current_active_user)):
    token = create_access_token(data={"sub": str(current_user.id), "role": current_user.role.value}, expires_delta=timedelta(minutes=30))
    return TokenResponse(access_token=token, user_id=current_user.id, role=current_user.role)

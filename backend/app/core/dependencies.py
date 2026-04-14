from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database import SessionLocal
from app.models.user import User, UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_error
    except Exception:
        raise credentials_error

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise credentials_error
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def require_standard_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != UserRole.user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User access required")
    return current_user

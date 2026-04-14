from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.cache import cache_delete, cache_get_json, cache_set_json
from app.core.dependencies import get_current_active_user, get_db, require_admin
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserRoleUpdate, UserStatusUpdate, UserUpdate


router = APIRouter()
admin_router = APIRouter()


@router.get("/me", response_model=UserResponse, summary="Get own profile")
def get_me(current_user: User = Depends(get_current_active_user)):
    cache_key = f"user_profile:{current_user.id}"
    try:
        cached = cache_get_json(cache_key)
        if cached:
            return cached
    except Exception:
        pass

    payload = UserResponse.model_validate(current_user).model_dump(mode="json")
    try:
        cache_set_json(cache_key, payload)
    except Exception:
        pass
    return payload


@router.put("/me", response_model=UserResponse, summary="Update own profile")
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updates = payload.model_dump(exclude_unset=True)
    if "username" in updates:
        existing = db.query(User).filter(User.username == updates["username"], User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

    for field, value in updates.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    try:
        cache_delete(f"user_profile:{current_user.id}")
    except Exception:
        pass
    return current_user


@admin_router.get("/", response_model=list[UserResponse], summary="Admin list users")
def list_users(
    search: str | None = Query(default=None, description="Search by email or username"),
    role: UserRole | None = Query(default=None, description="Filter by role"),
    is_active: bool | None = Query(default=None, description="Filter by active status"),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    query = db.query(User)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(or_(User.email.ilike(search_pattern), User.username.ilike(search_pattern)))
    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.order_by(User.created_at.desc()).all()


@admin_router.put("/{user_id}/role", response_model=UserResponse, summary="Admin change user role")
def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin_user.id and payload.role != UserRole.admin:
        raise HTTPException(status_code=400, detail="You cannot remove your own admin role")
    user.role = payload.role
    db.commit()
    db.refresh(user)
    try:
        cache_delete(f"user_profile:{user.id}")
    except Exception:
        pass
    return user


@admin_router.put("/{user_id}/status", response_model=UserResponse, summary="Admin activate/deactivate user")
def update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin_user.id and payload.is_active is False:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account")

    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    try:
        cache_delete(f"user_profile:{user.id}")
    except Exception:
        pass
    return user


@admin_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Admin remove user")
def remove_user(user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="You cannot remove your own account")

    cache_key = f"user_profile:{user.id}"
    db.delete(user)
    db.commit()
    try:
        cache_delete(cache_key)
    except Exception:
        pass
    return None

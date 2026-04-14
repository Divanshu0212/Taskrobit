from fastapi import APIRouter

from app.api.v1.endpoints import auth, tasks, users


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tasks.admin_router, prefix="/admin/tasks", tags=["Admin Tasks"])
api_router.include_router(users.admin_router, prefix="/admin/users", tags=["Admin Users"])

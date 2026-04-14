from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1.router import api_router
from app.config import get_settings
from app.database import engine


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    yield


app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Robust task management API with JWT auth and RBAC",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["System"])
def health_check():
    return {"success": True, "message": "Service healthy", "data": {"status": "ok"}}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    serialized_errors = []
    for error in exc.errors():
        normalized_error = dict(error)
        ctx = normalized_error.get("ctx")
        if isinstance(ctx, dict) and "error" in ctx:
            ctx["error"] = str(ctx["error"])
        serialized_errors.append(normalized_error)

    primary_message = "Validation error"
    if serialized_errors:
        msg = serialized_errors[0].get("msg")
        if isinstance(msg, str):
            primary_message = msg.replace("Value error, ", "")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": primary_message,
            "detail": primary_message,
            "errors": jsonable_encoder(serialized_errors),
        },
    )


@app.exception_handler(404)
async def not_found_handler(_: Request, __):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": "Resource not found", "error_code": "NOT_FOUND"},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(_: Request, __):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "error_code": "SERVER_ERROR"},
    )

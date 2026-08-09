from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.devices import router as devices_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.exceptions import (
    AppError,
    DeviceCodeAlreadyExistsError,
    DeviceNotFoundError,
    InvalidParameterError,
)

# 確保 SQLAlchemy 能找到所有 models
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 啟動時執行。
    若資料表不存在，會自動建立 devices table。
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="IoT 設備基本資料管理 API",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(devices_router)


@app.get(
    "/",
    tags=["Health"],
    summary="API 根目錄",
)
def root():
    return {
        "app": settings.app_name,
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="健康檢查",
)
def health():
    return {
        "status": "ok",
    }


@app.exception_handler(DeviceNotFoundError)
async def device_not_found_handler(
    request: Request,
    exc: DeviceNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(DeviceCodeAlreadyExistsError)
async def device_code_already_exists_handler(
    request: Request,
    exc: DeviceCodeAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(InvalidParameterError)
async def invalid_parameter_handler(
    request: Request,
    exc: InvalidParameterError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(AppError)
async def app_error_handler(
    request: Request,
    exc: AppError,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": exc.message,
        },
    )

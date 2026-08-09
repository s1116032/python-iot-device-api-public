from typing import Optional

from fastapi import APIRouter, Depends, Query, Response
from fastapi import status as http_status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import (
    DeviceCreate,
    DeviceListResponse,
    DeviceRead,
    DeviceStatisticsResponse,
    DeviceUpdate,
)
from app.services.device_service import DeviceService

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


def get_device_service(
    db: Session = Depends(get_db),
) -> DeviceService:
    repository = DeviceRepository(db)
    service = DeviceService(repository)

    return service


@router.post(
    "",
    response_model=DeviceRead,
    status_code=http_status.HTTP_201_CREATED,
    summary="新增設備",
    description="新增一筆 IoT 設備基本資料。",
)
def create_device(
    payload: DeviceCreate,
    service: DeviceService = Depends(get_device_service),
):
    return service.create_device(payload)


@router.get(
    "",
    response_model=DeviceListResponse,
    summary="查詢設備列表",
    description="支援依狀態、位置、設備類型、關鍵字查詢，並支援分頁。",
)
def list_devices(
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="設備狀態，例如 online / offline / maintenance",
    ),
    location: Optional[str] = Query(
        None,
        description="設備位置",
    ),
    device_type: Optional[str] = Query(
        None,
        description="設備類型，例如 sensor / gateway / camera",
    ),
    keyword: Optional[str] = Query(
        None,
        description="搜尋 device_code 或 device_name",
    ),
    page: int = Query(
        1,
        ge=1,
        description="頁碼",
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
        description="每頁筆數",
    ),
    service: DeviceService = Depends(get_device_service),
):
    return service.list_devices(
        status=status_filter,
        location=location,
        device_type=device_type,
        keyword=keyword,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/statistics",
    response_model=DeviceStatisticsResponse,
    summary="設備統計",
    description="依 status、location 或 device_type 分組統計設備數量。",
)
def get_device_statistics(
    group_by: str = Query(
        ...,
        description="分組欄位，可選 status / location / device_type",
    ),
    min_count: Optional[int] = Query(
        None,
        ge=0,
        description="最小數量，對應 SQL 的 HAVING COUNT(*) >= min_count",
    ),
    service: DeviceService = Depends(get_device_service),
):
    return service.get_statistics(
        group_by=group_by,
        min_count=min_count,
    )


@router.get(
    "/{device_id}",
    response_model=DeviceRead,
    summary="查詢單一設備",
    description="依照設備 id 查詢單一設備。",
)
def get_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
):
    return service.get_device(device_id)


@router.put(
    "/{device_id}",
    response_model=DeviceRead,
    summary="更新設備",
    description="更新指定設備資料，device_code 不可更新。",
)
def update_device(
    device_id: int,
    payload: DeviceUpdate,
    service: DeviceService = Depends(get_device_service),
):
    return service.update_device(device_id, payload)


@router.delete(
    "/{device_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    summary="刪除設備",
    description="刪除指定設備。",
)
def delete_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
):
    service.delete_device(device_id)

    return Response(status_code=http_status.HTTP_204_NO_CONTENT)

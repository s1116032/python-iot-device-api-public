from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class DeviceBase(BaseModel):
    device_code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="設備編號，例如 DEV-001",
    )

    device_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="設備名稱",
    )

    device_type: Optional[str] = Field(
        None,
        max_length=50,
        description="設備類型，例如 sensor / gateway / camera",
    )

    location: Optional[str] = Field(
        None,
        max_length=100,
        description="設備位置",
    )

    status: DeviceStatus = Field(
        DeviceStatus.OFFLINE,
        description="設備狀態",
    )

    ip_address: Optional[str] = Field(
        None,
        max_length=45,
        description="設備 IP，支援 IPv4 / IPv6",
    )


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    device_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="設備名稱",
    )

    device_type: Optional[str] = Field(
        None,
        max_length=50,
        description="設備類型",
    )

    location: Optional[str] = Field(
        None,
        max_length=100,
        description="設備位置",
    )

    status: Optional[DeviceStatus] = Field(
        None,
        description="設備狀態",
    )

    ip_address: Optional[str] = Field(
        None,
        max_length=45,
        description="設備 IP",
    )


class DeviceRead(BaseModel):
    id: int
    device_code: str
    device_name: str
    device_type: Optional[str]
    location: Optional[str]
    status: DeviceStatus
    ip_address: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[DeviceRead]


class DeviceStatisticsItem(BaseModel):
    label: str
    count: int


class DeviceStatisticsResponse(BaseModel):
    group_by: str
    items: List[DeviceStatisticsItem]

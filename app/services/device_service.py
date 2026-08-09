from typing import Optional

from app.exceptions import (
    DeviceCodeAlreadyExistsError,
    DeviceNotFoundError,
    InvalidParameterError,
)
from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import (
    DeviceCreate,
    DeviceListResponse,
    DeviceRead,
    DeviceStatisticsItem,
    DeviceStatisticsResponse,
    DeviceStatus,
    DeviceUpdate,
)


class DeviceService:
    ALLOWED_GROUP_BY_FIELDS = {
        "status",
        "location",
        "device_type",
    }

    MAX_PAGE_SIZE = 100

    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    def create_device(self, data: DeviceCreate) -> DeviceRead:
        existing_device = self.repository.get_by_code(data.device_code)

        if existing_device:
            raise DeviceCodeAlreadyExistsError(
                f"Device code '{data.device_code}' already exists"
            )

        device = self.repository.create(data)

        return DeviceRead.model_validate(device)

    def get_device(self, device_id: int) -> DeviceRead:
        device = self._get_device_or_raise(device_id)

        return DeviceRead.model_validate(device)

    def list_devices(
        self,
        status: Optional[str] = None,
        location: Optional[str] = None,
        device_type: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> DeviceListResponse:
        page, page_size = self._validate_pagination(page, page_size)

        status_value = self._validate_status(status)
        location_value = self._clean_string(location)
        device_type_value = self._clean_string(device_type)
        keyword_value = self._clean_string(keyword)

        devices, total = self.repository.list_devices(
            status=status_value,
            location=location_value,
            device_type=device_type_value,
            keyword=keyword_value,
            page=page,
            page_size=page_size,
        )

        items = [DeviceRead.model_validate(device) for device in devices]

        return DeviceListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=items,
        )

    def update_device(
        self,
        device_id: int,
        data: DeviceUpdate,
    ) -> DeviceRead:
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise InvalidParameterError("No fields to update")

        device = self._get_device_or_raise(device_id)

        updated_device = self.repository.update(device, data)

        return DeviceRead.model_validate(updated_device)

    def delete_device(self, device_id: int) -> None:
        device = self._get_device_or_raise(device_id)

        self.repository.delete(device)

    def get_statistics(
        self,
        group_by: str,
        min_count: Optional[int] = None,
    ) -> DeviceStatisticsResponse:
        group_by_value = self._clean_string(group_by)

        if group_by_value is None:
            raise InvalidParameterError("group_by is required")

        if group_by_value not in self.ALLOWED_GROUP_BY_FIELDS:
            raise InvalidParameterError(
                "group_by must be one of: status, location, device_type"
            )

        if min_count is not None and min_count < 0:
            raise InvalidParameterError("min_count must be greater than or equal to 0")

        rows = self.repository.group_counts(
            group_by=group_by_value,
            min_count=min_count,
        )

        items = [
            DeviceStatisticsItem(
                label=label,
                count=count,
            )
            for label, count in rows
        ]

        return DeviceStatisticsResponse(
            group_by=group_by_value,
            items=items,
        )

    def _get_device_or_raise(self, device_id: int) -> Device:
        device = self.repository.get_by_id(device_id)

        if device is None:
            raise DeviceNotFoundError(f"Device id {device_id} not found")

        return device

    def _validate_pagination(
        self,
        page: int,
        page_size: int,
    ) -> tuple[int, int]:
        if page < 1:
            raise InvalidParameterError("page must be greater than or equal to 1")

        if page_size < 1:
            raise InvalidParameterError("page_size must be greater than or equal to 1")

        if page_size > self.MAX_PAGE_SIZE:
            raise InvalidParameterError(
                f"page_size must be less than or equal to {self.MAX_PAGE_SIZE}"
            )

        return page, page_size

    def _validate_status(self, status: Optional[str]) -> Optional[str]:
        status_value = self._clean_string(status)

        if status_value is None:
            return None

        try:
            return DeviceStatus(status_value).value
        except ValueError:
            raise InvalidParameterError(
                "status must be one of: online, offline, maintenance"
            )

    @staticmethod
    def _clean_string(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value

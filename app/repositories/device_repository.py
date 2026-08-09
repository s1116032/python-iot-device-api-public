from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: DeviceCreate) -> Device:
        payload = data.model_dump(mode="json")

        device = Device(**payload)

        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)

        return device

    def get_by_id(self, device_id: int) -> Optional[Device]:
        stmt = select(Device).where(Device.id == device_id)

        return self.db.scalar(stmt)

    def get_by_code(self, device_code: str) -> Optional[Device]:
        stmt = select(Device).where(Device.device_code == device_code)

        return self.db.scalar(stmt)

    def list_devices(
        self,
        status: Optional[str] = None,
        location: Optional[str] = None,
        device_type: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Device], int]:
        stmt = select(Device)
        count_stmt = select(func.count(Device.id))

        stmt = self._apply_filters(
            stmt,
            status=status,
            location=location,
            device_type=device_type,
            keyword=keyword,
        )

        count_stmt = self._apply_filters(
            count_stmt,
            status=status,
            location=location,
            device_type=device_type,
            keyword=keyword,
        )

        total = self.db.scalar(count_stmt) or 0

        offset = (page - 1) * page_size

        stmt = (
            stmt.order_by(Device.created_at.desc(), Device.id.desc())
            .offset(offset)
            .limit(page_size)
        )

        devices = self.db.scalars(stmt).all()

        return devices, total

    def update(self, device: Device, data: DeviceUpdate) -> Device:
        payload = data.model_dump(exclude_unset=True, mode="json")

        for field, value in payload.items():
            setattr(device, field, value)

        self.db.commit()
        self.db.refresh(device)

        return device

    def delete(self, device: Device) -> None:
        self.db.delete(device)
        self.db.commit()

    def group_counts(
        self,
        group_by: str,
        min_count: Optional[int] = None,
    ) -> List[Tuple[str, int]]:
        group_columns = {
            "status": Device.status,
            "location": Device.location,
            "device_type": Device.device_type,
        }

        group_column = group_columns[group_by]

        stmt = (
            select(
                group_column.label("label"),
                func.count().label("count"),
            )
            .select_from(Device)
            .group_by(group_column)
        )

        if min_count is not None:
            stmt = stmt.having(func.count() >= min_count)

        rows = self.db.execute(stmt).all()

        result: List[Tuple[str, int]] = []

        for row in rows:
            label = row._mapping["label"]
            count = row._mapping["count"]

            if label is None:
                label = "unknown"

            result.append((str(label), int(count)))

        return result

    def _apply_filters(
        self,
        stmt,
        status: Optional[str] = None,
        location: Optional[str] = None,
        device_type: Optional[str] = None,
        keyword: Optional[str] = None,
    ):
        if status:
            stmt = stmt.where(Device.status == status)

        if location:
            stmt = stmt.where(Device.location == location)

        if device_type:
            stmt = stmt.where(Device.device_type == device_type)

        if keyword:
            pattern = f"%{keyword}%"

            stmt = stmt.where(
                or_(
                    Device.device_code.like(pattern),
                    Device.device_name.like(pattern),
                )
            )

        return stmt

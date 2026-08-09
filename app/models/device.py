from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    device_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    device_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    device_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        index=True,
        nullable=True,
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(100),
        index=True,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        index=True,
        nullable=False,
        default="offline",
        server_default="offline",
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"<Device("
            f"id={self.id}, "
            f"device_code='{self.device_code}', "
            f"device_name='{self.device_name}', "
            f"status='{self.status}'"
            f")>"
        )

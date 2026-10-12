from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class Warehouse(Base):
    __tablename__='warehouses'
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(150))
    location: Mapped[str]=mapped_column(String(255))
    capacity: Mapped[int]=mapped_column(Integer)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
class WarehouseAccess(Base):
    __tablename__='warehouse_access'
    __table_args__=(UniqueConstraint('user_id','warehouse_id'),)
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    warehouse_id: Mapped[int]=mapped_column(ForeignKey('warehouses.id', ondelete='CASCADE'), index=True)

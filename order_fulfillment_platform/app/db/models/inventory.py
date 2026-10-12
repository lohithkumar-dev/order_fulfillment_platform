import enum
from datetime import datetime, timezone
from sqlalchemy import Enum, Integer, DateTime, ForeignKey, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class InventoryTransactionType(str, enum.Enum):
    RECEIPT='receipt'; ADJUSTMENT='adjustment'; RESERVATION='reservation'; RELEASE='release'; SALE='sale'; RETURN='return'; TRANSFER_OUT='transfer_out'; TRANSFER_IN='transfer_in'
class Inventory(Base):
    __tablename__='inventory'
    __table_args__=(UniqueConstraint('warehouse_id','product_id'),)
    id: Mapped[int]=mapped_column(primary_key=True)
    warehouse_id: Mapped[int]=mapped_column(ForeignKey('warehouses.id', ondelete='CASCADE'), index=True)
    product_id: Mapped[int]=mapped_column(ForeignKey('products.id', ondelete='CASCADE'), index=True)
    quantity: Mapped[int]=mapped_column(Integer, default=0)
    reserved_quantity: Mapped[int]=mapped_column(Integer, default=0)
    reorder_threshold: Mapped[int]=mapped_column(Integer, default=10)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
class InventoryTransaction(Base):
    __tablename__='inventory_transactions'
    id: Mapped[int]=mapped_column(primary_key=True)
    product_id: Mapped[int]=mapped_column(ForeignKey('products.id'), index=True)
    warehouse_id: Mapped[int]=mapped_column(ForeignKey('warehouses.id'), index=True)
    transaction_type: Mapped[InventoryTransactionType]=mapped_column(Enum(InventoryTransactionType), index=True)
    quantity: Mapped[int]=mapped_column(Integer)
    reference_entity: Mapped[str|None]=mapped_column(String(80))
    reference_id: Mapped[str|None]=mapped_column(String(80))
    user_id: Mapped[int|None]=mapped_column(ForeignKey('users.id'))
    metadata_json: Mapped[dict|None]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

import enum
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Enum, DateTime, ForeignKey, Numeric, String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class OrderStatus(str, enum.Enum):
    PENDING='pending'; CONFIRMED='confirmed'; ASSIGNED='assigned'; PROCESSING='processing'; SHIPPED='shipped'; DELIVERED='delivered'; CANCELLED='cancelled'
class PaymentStatus(str, enum.Enum): PENDING='pending'; PAID='paid'; FAILED='failed'; REFUNDED='refunded'
class Order(Base):
    __tablename__='orders'
    id: Mapped[int]=mapped_column(primary_key=True)
    order_number: Mapped[str]=mapped_column(String(40), unique=True, index=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey('users.id'), index=True)
    warehouse_id: Mapped[int]=mapped_column(ForeignKey('warehouses.id'), index=True)
    fulfillment_agent_id: Mapped[int|None]=mapped_column(ForeignKey('users.id'), index=True)
    total_amount: Mapped[Decimal]=mapped_column(Numeric(12,2), default=0)
    status: Mapped[OrderStatus]=mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    payment_status: Mapped[PaymentStatus]=mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    expected_delivery_date: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
class OrderItem(Base):
    __tablename__='order_items'
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), index=True)
    product_id: Mapped[int]=mapped_column(ForeignKey('products.id'), index=True)
    quantity: Mapped[int]=mapped_column(Integer)
    unit_price: Mapped[Decimal]=mapped_column(Numeric(12,2))
    discount: Mapped[Decimal]=mapped_column(Numeric(12,2), default=0)
    tax: Mapped[Decimal]=mapped_column(Numeric(12,2), default=0)
    total: Mapped[Decimal]=mapped_column(Numeric(12,2))
class OrderStatusHistory(Base):
    __tablename__='order_status_history'
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), index=True)
    from_status: Mapped[str|None]=mapped_column(String(30))
    to_status: Mapped[str]=mapped_column(String(30))
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id'))
    metadata_json: Mapped[dict|None]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

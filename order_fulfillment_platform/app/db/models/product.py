from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import String, Text, Boolean, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class Product(Base):
    __tablename__='products'
    id: Mapped[int]=mapped_column(primary_key=True)
    sku: Mapped[str]=mapped_column(String(80), unique=True, index=True)
    name: Mapped[str]=mapped_column(String(200), index=True)
    description: Mapped[str|None]=mapped_column(Text)
    category: Mapped[str|None]=mapped_column(String(100), index=True)
    price: Mapped[Decimal]=mapped_column(Numeric(12,2))
    cost_price: Mapped[Decimal]=mapped_column(Numeric(12,2))
    is_active: Mapped[bool]=mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

import enum
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Role(str, enum.Enum):
    ADMIN='admin'; WAREHOUSE_MANAGER='warehouse_manager'; FULFILLMENT_AGENT='fulfillment_agent'; CUSTOMER='customer'
class User(Base):
    __tablename__='users'
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str]=mapped_column(String(150))
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[Role]=mapped_column(Enum(Role), default=Role.CUSTOMER, index=True)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

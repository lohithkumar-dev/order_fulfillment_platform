import enum
from datetime import datetime, timezone
from sqlalchemy import Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class ReturnStatus(str, enum.Enum): REQUESTED='requested'; APPROVED='approved'; REJECTED='rejected'; RECEIVED='received'; COMPLETED='completed'
class Return(Base):
    __tablename__='returns'
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey('orders.id'), index=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey('users.id'), index=True)
    status: Mapped[ReturnStatus]=mapped_column(Enum(ReturnStatus), default=ReturnStatus.REQUESTED, index=True)
    reason: Mapped[str]=mapped_column(String(500))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
class ReturnItem(Base):
    __tablename__='return_items'
    id: Mapped[int]=mapped_column(primary_key=True)
    return_id: Mapped[int]=mapped_column(ForeignKey('returns.id', ondelete='CASCADE'))
    product_id: Mapped[int]=mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int]=mapped_column(Integer)

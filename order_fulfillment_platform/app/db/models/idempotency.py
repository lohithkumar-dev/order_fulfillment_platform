from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class IdempotencyKey(Base):
    __tablename__='idempotency_keys'
    __table_args__=(UniqueConstraint('user_id','key'),)
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(Integer, index=True)
    key: Mapped[str]=mapped_column(String(255))
    response_status: Mapped[int|None]=mapped_column(Integer)
    response_body: Mapped[dict|None]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

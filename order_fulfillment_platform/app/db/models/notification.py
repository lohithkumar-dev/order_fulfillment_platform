from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class Notification(Base):
    __tablename__='notifications'
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    event_type: Mapped[str]=mapped_column(String(80), index=True)
    message: Mapped[str]=mapped_column(String(500))
    payload: Mapped[dict|None]=mapped_column(JSON)
    is_read: Mapped[bool]=mapped_column(Boolean, default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

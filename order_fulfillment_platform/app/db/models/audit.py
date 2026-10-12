from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class AuditLog(Base):
    __tablename__='audit_logs'
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int|None]=mapped_column(ForeignKey('users.id'))
    action: Mapped[str]=mapped_column(String(100), index=True)
    entity: Mapped[str]=mapped_column(String(80), index=True)
    entity_id: Mapped[str|None]=mapped_column(String(80))
    ip_address: Mapped[str|None]=mapped_column(String(64))
    metadata_json: Mapped[dict|None]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

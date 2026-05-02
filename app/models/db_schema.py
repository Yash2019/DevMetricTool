from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import JSON, DateTime

class WebhookEvent(Base):
    __tablename__ = 'webhook_events'

    id: Mapped[int] =  mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(nullable=True)
    delivery_id: Mapped[str] = mapped_column(nullable=True)
    action:Mapped[str] = mapped_column(nullable=True)
    payload:Mapped[dict] = mapped_column(JSON)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
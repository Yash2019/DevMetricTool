from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_schema import WebhookEvent
from datetime import datetime, timezone


async def receive_json(request: Request, db: AsyncSession):

    payload = await request.json()  #Parse the incoming request
    event_type = request.headers.get("X-GitHub-Event")
    delivery_id = request.headers.get("X-GitHub-Delivery")
    action = request.get("action")

    event = WebhookEvent(
        event_type=event_type,
        delivery_id=delivery_id,
        action=action,
        payload=payload,
        received_at=datetime.now(timezone.utc)
    )

    db.add(event)
    await db.commit()
    await db.refresh(event)

    return {
        'status': 'received',
        'event_id': event.id
    }

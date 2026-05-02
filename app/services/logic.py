from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_schema import WebhookEvent
from datetime import datetime, timezone
import hmac
import hashlib
import json 
from app.configure import config


def verify_signature(raw_data: bytes, secret: str, signature_header: str):
    expected = 'sha256=' + hmac.new(
        key=secret.encode(),
        msg=raw_data,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature_header)

async def receive_json(request: Request, db: AsyncSession):

    raw_body = await request.body()  # read the raw bytes

    if not raw_body:
        raise HTTPException(status_code=400, detail="Empty body")
    
    payload = json.loads(raw_body)  #parse the raw byte to json 
    
    signature = request.headers.get("X-Hub-Signature-256")

    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    if not verify_signature(raw_body,config.SECRET, signature_header=signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event_type = request.headers.get("X-GitHub-Event")
    delivery_id = request.headers.get("X-GitHub-Delivery")
    action = payload.get("action")


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
        "status": "received",
        "event_id": event.id,
        "event_type": event.event_type,
        "delivery_id": event.delivery_id,
        "action": event.action,
        "received_at": event.received_at,
    }


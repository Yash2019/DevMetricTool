from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_schema import WebhookEvent
from sqlalchemy import select
from datetime import datetime, timedelta, timezone


async def compute_commits(db: AsyncSession):
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)

    stmt =  select(WebhookEvent).where(
        WebhookEvent.event_type == 'push',
        WebhookEvent.received_at >= cutoff_time
    )
    result = await db.execute(stmt)
    events = result.scalars().all()

    num_commits = 0

    for event in events:
        payload = event.payload or {}
        commit = payload.get('commits', [])
        num_commits += len(commit)

    return num_commits
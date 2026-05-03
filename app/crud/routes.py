from app.services.logic import receive_json
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from app.database.db import get_db
from app.services.compute_metric import compute_commits

router = APIRouter()

@router.post('/webhook')
async def receive_data_endpoint(request: Request, db: AsyncSession = Depends(get_db)):
    return await receive_json(request, db)


@router.get('/Commit_metric')
async def commit_metric_endpoint(db: AsyncSession = Depends(get_db)):
    return await compute_commits(db)

@router.get('/test')
async def tedstfunc():
    return {'message': 'return'}




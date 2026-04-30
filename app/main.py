from fastapi import FastAPI
from app.database.db import create_table
from app.crud.routes import router


app = FastAPI()

@app.on_event('startup')
async def on_startup() -> None:
    await create_table()

app.include_router(
    router
)
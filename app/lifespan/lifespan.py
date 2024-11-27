from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.lifespan import init_db, delete_data


@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    DB内のデータを初期化
    """
    delete_data.delete_data()
    init_db.init_db()
    yield
    






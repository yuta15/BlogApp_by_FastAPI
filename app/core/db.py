from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel
from core.setting import setting

db_url = setting.DB_URL
engin = create_engine(db_url)


def get_db():
    with Session(engin) as session:
        yield session
    
    
def create_db_and_table():
    SQLModel.metadata.create_all(engin)
    
    
def drop_db_and_table():
    SQLModel.metadata.drop_all(engin)
    
    
def init_db():
    drop_db_and_table()
    create_db_and_table()
    
    
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

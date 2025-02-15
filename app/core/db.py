from sqlmodel import Session, create_engine, SQLModel
import os

from app.core.setting import setting
from app.models.User import User
from app.models.Article import Article


db_url = setting.DB_URL
engin = create_engine(db_url)


def get_db():
    with Session(engin) as session:
        yield session


def create_table():
    """
    tableを作成する関数
    """
    env = os.environ.get('Env')
    if env == 'Dev' or env == 'Testing':
        SQLModel.metadata.create_all(engin)
    
    
def drop_table():
    """
    tableを削除する関数
    """
    env = os.environ.get('Env')
    if env == 'Dev' or env == 'Testing':
        SQLModel.metadata.drop_all(engin)
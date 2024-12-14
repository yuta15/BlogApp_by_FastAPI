from sqlmodel import Session, create_engine, delete
import logging

from app.core.setting import setting
from app.models.User import User
from app.models.Article import Article

def delete_data():
    engin = create_engine(setting.DB_URL)
    try:
        with Session(engin) as session:
            stmt = delete(User)
            session.exec(stmt)
            session.commit()
            stmt = delete(Article)
            session.exec(stmt)
            session.commit()
    except Exception as e:
        raise e
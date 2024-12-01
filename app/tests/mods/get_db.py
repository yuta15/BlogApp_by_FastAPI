from sqlmodel import Session, create_engine, SQLModel

from app.core.setting import setting


engin = create_engine(setting.DB_URL)


def create_table():
    SQLModel.metadata.create_all(engin)


def get_db():
    with Session(engin) as session:
        yield session
    
from sqlmodel import Session, create_engine

from app.core.setting import setting


def get_db():
    engin = create_engine(setting.DB_URL)
    with Session(engin) as session:
        yield session
    
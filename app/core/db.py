from sqlmodel import Session, create_engine, SQLModel

from app.core.setting import setting

db_url = setting.DB_URL
engin = create_engine(db_url)


def get_db():
    with Session(engin) as session:
        yield session

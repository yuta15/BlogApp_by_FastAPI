from sqlmodel import select, create_engine, Session
from app.models.User import User



db_url = f'mysql+pymysql://testuser:testuser1234@172.18.0.100:3306/main'

def get_db():
    with Session(engin) as session:
        yield session

engin = create_engine(db_url)
session = next(get_db())
stmt = select(User)
results = session.exec(stmt)

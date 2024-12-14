from contextlib import asynccontextmanager
from sqlmodel import Session, create_engine

from app.core.setting import setting
from app.lifespan.init_data import user_init_data
from app.models.User import User


engin = create_engine(url=setting.DB_URL)

@asynccontextmanager
def init_db():
    """
    初期データをインサートする関数
    """
    try:
        with Session(engin) as session:
            users = []
            for user in user_init_data:
                users.append(User.model_validate(user))
                
            session.add_all(users)
            session.commit()
    except Exception as e:
        raise e
    
    
    
    
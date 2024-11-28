from contextlib import asynccontextmanager
from sqlmodel import Session, create_engine

from app.core.setting import setting
from app.lifespan.init_data import user_init_data, superuser_init_data
from app.models.user.user_models import User
from app.models.superuser.superuser import Superuser


engin = create_engine(url=setting.DB_URL)

@asynccontextmanager
def init_db():
    """
    初期データをインサートする関数
    """
    try:
        with Session(engin) as session:
            users = []
            superusers = []
            for user, superuser in zip(user_init_data, superuser_init_data):
                users.append(User.model_validate(user))
                superusers.append(Superuser.model_validate(superuser))
                
            session.add_all(users)
            session.add_all(superusers)
            session.commit()
    except Exception as e:
        raise e
    
    
    
    
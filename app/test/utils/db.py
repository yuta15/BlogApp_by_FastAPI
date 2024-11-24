from datetime import datetime
from sqlmodel import SQLModel, Session
from typing import List
from uuid import uuid4

from app.core.db import engin, get_db
from app.core.setting import setting
from app.core.security import PWD_CONTEXT
from app.models.user_models import User
from app.test.init_data import init_users_data




def create_insert_users(user_datas: List[object]):
    """
    args
        user_datas: List[object]
            objectには、username, password, emailを含めてください。
    """
    users: List[User] = []
    for user_data in user_datas:
        users.append(
            User.model_validate(
                user_data,
                update={
                    'uuid': uuid4(),
                    'create_at': datetime.now(setting.TZ),
                    'update_at': datetime.now(setting.TZ),
                    'hashed_password': PWD_CONTEXT.hash(user_data.get('password'))
                }
            )
        )
    return users


def create_db_and_table():
    SQLModel.metadata.create_all(engin)
    
    
def drop_db_and_table():
    SQLModel.metadata.drop_all(engin)
    
    
def insert_data(users: List[User]):
    with Session(engin) as session:
        for user in users:
            session.add(user)
            session.commit()
            
    
def db_init():
    drop_db_and_table()
    create_db_and_table()
    test_users = create_insert_users(init_users_data)
    insert_data(test_users)

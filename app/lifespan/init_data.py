from uuid import uuid4
from datetime import datetime
from passlib.context import CryptContext

from app.core.setting import setting


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
user_init_data = [
    {
        'uuid': uuid4(),
        'create_at': datetime.now(setting.TZ),
        'update_at': datetime.now(setting.TZ),
        'username': 'user1', 
        'hashed_password': pwd_context.hash('user1password'),
        'email': 'user1@example.com'
    },
    {
        'uuid': uuid4(),
        'create_at': datetime.now(setting.TZ),
        'update_at': datetime.now(setting.TZ),
        'username': 'user2', 
        'hashed_password': pwd_context.hash('user2password'),
        'email': 'user2@example.com'
    },
    {
        'uuid': uuid4(),
        'create_at': datetime.now(setting.TZ),
        'update_at': datetime.now(setting.TZ),
        'username': 'user3', 
        'hashed_password': pwd_context.hash('user3password'),
        'email': 'user3@example.com'
    },
]
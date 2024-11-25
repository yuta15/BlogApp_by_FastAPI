from uuid import uuid4
from datetime import datetime

from app.core.setting import setting
from app.core.security import create_password_hash
from app.models.superuser.superuser import Superuser, SuperuserInput


def create_superuser_params(superuser_input: SuperuserInput):
    """
    DB投入用にvalidationするための関数
    """
    superuser: Superuser = Superuser.model_validate(
        {
            'username': superuser_input.username.encode('utf-8'),
            'email': superuser_input.email.encode('utf-8'),
            'uuid': uuid4(),
            'create_at': datetime.now(setting.TZ),
            'update_at': datetime.now(setting.TZ),
            'hashed_password': create_password_hash(superuser_input.password),
        }
    )
    return superuser
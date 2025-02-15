import uuid
import datetime
from passlib.context import CryptContext
import random
import string
import itertools

from app.models.User import User


def create_success_users(
    number: int = 1, 
    is_only_admin_user: bool = False,
    is_only_normal_user: bool = False,
    is_only_active_user: bool = False,
    is_only_inactive_user: bool = False,
    ) -> User:
    """
    ユーザーを生成する関数。
    正常にinsert可能な一般ユーザーを生成する。

    Args:
        number: int = 1
            - 作成するユーザーの数を指定
        is_only_admin_user: bool = False,
            - adminユーザーのみを作成
        is_only_normal_user: bool=False,
            - ノーマルユーザーのみを作成
        is_only_active_user: bool = False,
            - activeなユーザーのみを作成
        is_only_inactive_user: bool = False,
            - inactiveなユーザーのみを作成
            
        ex)
        active admin userのみを作成したい場合は以下のようにすることで指定可能。
        is_only_admin_user=True, is_only_active_user=True
        デフォルトでは全パターンのユーザーを作成する。
    Return:
        List[User]
    """
    insert_users = []
    if is_only_admin_user and is_only_active_user:
        pattern = [(1, 1)]
    elif is_only_normal_user and is_only_active_user:
        pattern = [(1, 0)]
    elif is_only_admin_user and is_only_inactive_user:
        pattern = [(0, 1)]
    elif is_only_normal_user and is_only_inactive_user:
        pattern = [(0, 0)]
    elif is_only_admin_user:
        pattern = [(1, 1), (0, 1)]
    elif is_only_normal_user:
        pattern = [(1, 0), (0, 0)]
    elif is_only_active_user:
        pattern = [(1, 1), (1, 0)]
    elif is_only_inactive_user:
        pattern = [(0, 1), (0, 0)]
    else:
        pattern = list(itertools.product([0, 1], repeat=2))
    
    while len(insert_users) < number:
        if len(insert_users) != 0:
            active_num = pattern[len(insert_users) % len(pattern)][0]
            admin_num = pattern[len(insert_users) % len(pattern)][0]
        else:
            active_num = pattern[0][0]
            admin_num = pattern[0][0]
            
        PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
        now = datetime.datetime.now()
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        insert_user = User.model_validate(
            {
                'username': username,
                'uuid': uuid.uuid4(),
                'create_at': now,
                'update_at': now,
                'hashed_password': PWD_CONTEXT.hash(password),
                'email': f'{username}@gmail.com',
                'is_active': bool(active_num),
                'is_admin': bool(admin_num)
            }
        )
        insert_users.append(insert_user)
    return insert_users
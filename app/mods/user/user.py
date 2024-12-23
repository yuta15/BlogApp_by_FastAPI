from datetime import datetime
from typing import List
import jwt

from app.mods.user.db import (fetch_users, generate_hashed_password, insert_user)
from app.mods.user.auth import (decode_token, generate_payload, verify_password)
from app.mods.user.data import (sanitize_to_utf8)
from app.models.User import User, UserRegister, UserLogin
from app.core.setting import setting
from app.deps.crud import SessionDeps

# db
def generate_user(user_params: UserRegister) -> User:
    """
    Insert可能なデータを生成するための関数
    """
    sanitized_params:dict = sanitize_to_utf8.sanitize_to_utf8(username=user_params.username, email=user_params.email)
    hashed_password: str = generate_hashed_password.generate_hash_password(user_params.password)
    current_time = datetime.now(setting.TZ)
    try:
        user: User = User.model_validate(
            {
                'username': sanitized_params.get('username'),
                'email': sanitized_params.get('email'),
                'create_at': current_time,
                'update_at': current_time,
                'hashed_password': hashed_password,
                'is_active': True,
                'is_admin': False
            },
        )
    except ValueError:
        return None
    else:
        return user
    

def create_user(session: SessionDeps, user_params: User) -> bool:
    """
    DBへのinsert処理を実行
    
    """
    is_result = insert_user.insert_user(session=session, user_params=user_params)
    return is_result


def check_fetch_users(users: any) -> any:
    """
    DBから取得したデータの内容の整合性を確認する
    """
    if len(users) == 0:
        return False
    elif not users:
        return None
    else:
        return users


def fetch_user_data(*,session: SessionDeps, **kwargs) -> User | None | bool:
    """
    単一のユーザー情報を取得するための関数
    
    return:
        User: DB内にユーザー情報が存在した場合
        None: DB内に該当のユーザー情報が存在しない場合
        bool: 処理内でエラーが発生し、ユーザー情報が取得できなかった場合はFalseを返す
    """
    try:
        users: List[User] | bool = fetch_users.fetch_users(session=session, **kwargs)
    except:
        return False
    else:
        if len(users) == 0:
            return None
        else:
            return users[0]


def fetch_users_data(*, session: SessionDeps,**kwargs) -> List[User | None] | bool:
    """
    複数のユーザー情報を取得するための関数
    
    return:
        List[User | None | bool]
        User: DB内にユーザー情報が存在した場合
        None: DB内に該当のユーザー情報が存在しない場合
        bool: 処理内でエラーが発生し、ユーザー情報が取得できなかった場合はFalseを返す
    """
    users: List[User | None] | bool = fetch_users.fetch_users(session=session, **kwargs)
    return users


def auth_user(*, session:SessionDeps, user_params: UserLogin) -> bool:
    """
    認証処理用の関数
    return:
        True: 認証成功
        False: 認証失敗
    """
    user = fetch_user_data(session=session, username=user_params.username)
    if user is None or not user or not user.is_active:
        return False, None
    is_valid = verify_password.verify_password(user_params.password, user.hashed_password)
    return is_valid, user


def take_subject_from_token(token) -> dict | None:
    """
    Tokenをデコードし、Subjectを取り出すための関数
    デコードの失敗、超過している場合はNoneを返す。
    """
    subject: dict = decode_token.decode_token(token)
    return subject


def comfirm_not_exist_user(*, session: SessionDeps, user_params: UserRegister) -> bool:
    """
    ユーザーが入力したユーザー名、emailデータがすでに使用されていないことを確認する。
    """
    try:
        users: List[User] = fetch_users.fetch_users(
            session=session, 
            username=user_params.username, 
            email=user_params.email
            )
    except:
        return False
    else:
        if len(users) == 0:
            return True
        else:
            return False


def create_token(user_params: User) -> str:
    """
    Token生成用関数
    """
    payload: dict = generate_payload.generate_payload(user_params=user_params)
    token: str = jwt.encode(payload=payload, key=setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return token
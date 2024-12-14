from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.func.check import check_password
from app.models.user.user_models import User



def auth_user(
    input_password: str,
    user: User
    ) -> None:
    """
    password情報の検証を実施する。
    args:
        input_password: str
            ユーザーから受け取ったパスワード情報
        
        user: User
            DBからfetchしたユーザー情報
    return:
        None
    Exception:
        HTTP_400_BAD_REQUEST
            検証に失敗した場合は、HTTP_400_BAD_REQUESTがリターンされる。
    """
    # 仮に複数存在した場合なValidationErrorになる。
    is_valid = check_password.check_password(input_password, user.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Bad Request')

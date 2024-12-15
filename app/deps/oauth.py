from fastapi.security import OAuth2PasswordBearer 
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import Session
from typing import List

from app.deps.crud import get_db
from app.mods.user.user import take_subject_from_token, fetch_user_data
from app.models.User import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def resolve_user_from_token(
    *,
    session: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
    ) -> User:
    """
    Token情報からToken情報を取得する。
    """
    subject = take_subject_from_token(token=token)
    user: User | None = fetch_user_data(session=session, username=subject.get('username'))
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    return user
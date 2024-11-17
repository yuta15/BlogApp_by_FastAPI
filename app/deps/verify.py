from fastapi import Depends, HTTPException
from typing import Union

from models.db_models import UserOutput
from deps import crud


def verify_used_username(session: crud.SessionDeps, username: str):
    """
    ユーザー名が使用されていないか確認する関数。
    """
    user: Union[UserOutput, None] = crud.fetch_user_by_username(session=session, username=username)
    return user


def verify_used_email(session: crud.SessionDeps, email: str):
    """
    emailが使用されていないか確認する関数。
    """
    user: Union[UserOutput, None] = crud.fetch_user_by_email(session=session, email=email)
    return user


def verify_userd_params(*, session: crud.SessionDeps, username: str | None, email: str | None):
    """
    ユーザー名とemailがすでに使用されていないことを確認する関数。
    """
    if username is not None:
        veried_username = verify_used_username(session=session, username=username)
    if email is not None:
        veried_email = verify_used_email(session=session, email=email)
    
    if veried_username is None and veried_email is None:
        return True
    else:
        return False

from fastapi import APIRouter, HTTPException

from app.models.user.user_models import SchemaUserRegisterInput, SchemaUserRegisterOutput, User
from app.deps.crud import SessionDeps
from app.mods.user.check_exist_user import check_exist_user
from app.mods.user.create_user import create_user


router = APIRouter(
    prefix='/user',
    tags=['user'],
)



@router.post('/register')
async def register(
    session: SessionDeps, 
    user_input:SchemaUserRegisterInput
    ):
    """
    ユーザー新規登録用API
    """
    check_exist_user(session=session, user_input=user_input)
    create_user(session=session, user_input=user_input)
    return {'detail': 'user create successfully'}



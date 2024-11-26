from fastapi import APIRouter, Depends

from app.deps.oauth import oauth2_scheme_suseruser
from app.deps.crud import SessionDeps
from app.models.superuser.superuser import Superuser, SuperuserInput
from app.mods.superuser import create_superuser, check_exist_superuser


router = APIRouter(
    prefix='/management',
    tags=['management'],
    dependencies=[Depends(oauth2_scheme_suseruser)]
)


@router.post('/register')
async def superuser_register(
    session: SessionDeps, 
    new_superuser_input: SuperuserInput
    ):
    """
    Superuserの新規ユーザー作成用API
    """
    check_exist_superuser.check_exist_user(session=session, user_input=new_superuser_input)
    create_superuser.create_superuser(session=session, input_user=new_superuser_input)
    return {'detail': 'user create successfully'}
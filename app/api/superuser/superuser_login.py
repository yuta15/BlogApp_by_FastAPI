from fastapi import APIRouter

from app.deps.crud import SessionDeps
from app.models.superuser.superuser import SuperuserInput, Superuser
from app.mods.superuser import fetch_superuser, auth_superuser, create_token


router = APIRouter(
    prefix='/superuser',
    tags=['superuser']
)


@router.post('/')
async def login(*, session: SessionDeps, superuser: SuperuserInput):
    fetched_superuser: Superuser = fetch_superuser.fetch_superuser(session=session, input_username=superuser.username)
    auth_superuser.auth_user(input_password=superuser.password, user=fetched_superuser)
    token: str = create_token.create_token(fetched_superuser)
    return {'access_token':token, 'token_type':"bearer"}
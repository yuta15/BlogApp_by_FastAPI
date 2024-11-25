from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT

from app.deps.oauth import oauth2_scheme_suseruser
from app.deps.crud import SessionDeps
from app.models.superuser.superuser import Superuser, SuperuserInput
from app.utils import verify, crud, superuser_create


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
    veried_result: bool = verify.is_user_info_available(
        table_model=Superuser,
        session=session,
        username=new_superuser_input.username,
        email=new_superuser_input.email
        )

    if not veried_result:
        HTTPException(status_code=HTTP_409_CONFLICT, detail='Username or e-mail is conflict')
    superuser: Superuser = superuser_create.create_superuser_params(superuser_input=new_superuser_input)
    crud.create_user(session=session, user_params=superuser)
    return superuser
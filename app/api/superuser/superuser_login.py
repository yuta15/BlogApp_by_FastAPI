from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from app.deps.crud import SessionDeps
from app.models.superuser.superuser import SuperuserInput, Superuser
from app.utils.verify import is_user_info_available
from app.utils import resolve, crud, verify
from app.core import security

router = APIRouter(
    prefix='/superuser',
    tags=['superuser']
)

@router.post('/')
async def login(*, session: SessionDeps, superuser: SuperuserInput):
    fetched_superuser: Superuser | None = crud.fetch_users(
        session=session, 
        table_model=Superuser, 
        username=superuser.username
        )
    if not fetched_superuser:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f'${superuser.username} is not exist user')
    
    is_auth: bool = verify.verify_user_credentials(
        fetched_user=fetched_superuser,
        hashed_password=superuser.password
    )
    
    if not is_auth:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Unauthorized User')
    
    token = security.generate_token(
        username=fetched_superuser.username, 
        email=fetched_superuser.email
        )
    return {"access_token": token, "token_type": "bearer"}
    
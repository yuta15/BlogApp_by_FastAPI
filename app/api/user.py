
from fastapi import APIRouter, Depends, HTTPException

from models.user_models import SchemaUserRegisterInput, SchemaUserRegisterOutput
from deps.crud import SessionDeps, create_user, fetch_users
from deps import verify


router = APIRouter(
    prefix='/user',
    tags=['user'],
)

@router.post('/register')
async def register(session: SessionDeps, user_input:SchemaUserRegisterInput) -> SchemaUserRegisterOutput:
    veried_result = verify.is_user_info_available(
        session=session, 
        username=user_input.username, 
        email=user_input.email
        )
    if not veried_result:
        raise HTTPException(status_code=409, detail='Username or e-mail is conflict')
    
    output_user = create_user(session=session, user=user_input)
    return output_user



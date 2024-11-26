from app.deps.crud import SessionDeps
from app.func.generate.generate_hash_password import generate_hash_password
from app.func.generate.generate_user import generate_user
from app.func.insert.insert_user import insert_user
from app.models.superuser.superuser import Superuser, SuperuserInput

def create_superuser(
    *,
    session: SessionDeps,
    input_user: SuperuserInput,
    ) -> None:
    hashed_password = generate_hash_password(input_user.password)
    user: Superuser = generate_user(
        username=input_user,
        email=input_user.email,
        hashed_password=hashed_password
    )
    
    insert_user(session=session, user=user)
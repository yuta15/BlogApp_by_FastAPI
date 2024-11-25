from app.deps.crud import SessionDeps
from app.func.generate.generate_hash_password import generate_hash_password
from app.func.generate.generate_user import generate_user
from app.func.insert.insert_user import insert_user
from app.models.user.user_models import SchemaUserRegisterInput, User


def create_user(
    *,
    session: SessionDeps,
    user_input: SchemaUserRegisterInput,
    ) -> None:
    hashed_password = generate_hash_password(user_input.password)
    user: User = generate_user(
        username=user_input.username,
        email=user_input.email,
        hashed_password=hashed_password
    )
    
    insert_user(session=session, user=user)
from fastapi import APIRouter, Depends

from app.deps.crud import SessionDeps
from app.deps.oauth import oauth2_scheme
from app.mods.user import resolve_user_from_token
from app.models.user.article_models import SchemaArticleInput
from app.models.user.user_models import User
from app.mods.user.create_new_article import create_new_article

router = APIRouter(
    prefix='/article',
    tags=['article'],
    # dependencies=[Depends(oauth2_scheme)]
)


@router.post('/new')
async def new_article(
    *, 
    session: SessionDeps,
    article:SchemaArticleInput, 
    user:User = Depends(resolve_user_from_token.resolve_user_from_token)
    ):
    create_new_article(session=session, article=article, user=user)
    return {'detail': 'new article create successfully'}
    



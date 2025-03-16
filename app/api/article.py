from fastapi import APIRouter
from sqlmodel import Session


from app.deps.crud import SessionDeps
from app.models.Article import Article
from app.mods.db.select import select


article = APIRouter(
    prefix='/article',
    tags=['article']
)


@article.get('/')
async def list_articles(session:SessionDeps, offset:int=0, limit:int=10):
    """
    article一覧を取得するための関数
    limitを指定することで指定の量の記事を取得することが可能。
    
    args:
        Session:SessionDeps
        offset: int = 0
            取得したい記事の最初の項番
        limit: int = 10
            取得したい記事の最後の項番
    return:
        articles: json
            - aritcle_id
            - user_id
            - username
            - title
            - created_at
            - updated_at
            metaデータのみの記事一覧
    """
    articles = select(session=session, model=Article, offset=offset, limit=limit)
    return articles


@article.get('/list')
async def fetch_article(Session:SessionDeps, id):
    """
    特定の記事の情報を取得するAPI
    args:
        Session:SessionDeps
        id: uuid
            articleのID情報
    return:
        article: json
            - article_id
            - created_at
            - updated_at
            - title
            - user_id
            - username
            - content
    """
    pass


@article.get('/search')
async def search_articles(Session:SessionDeps, search_requirement: list):
    """
    検索条件に応じて記事を検索するAPI
    args:
        Session:SessionDeps
        requirement: List
            検索条件をリスト形式で記述したもの
            ex)
                ['username:==test1', 'created_at:==2025/03/10']
                以下をキーにすることが可能
                username
                created_at
                updated_at
                uuid
    return:
        articles: json
            - aritcle_id
            - user_id
            - username
            - title
            - created_at
            - updated_at
    """
    pass


@article.post('/create')
async def create_aritcle(Session:SessionDeps, title: str, content: str):
    """
    新しい記事を投稿する機能
    args:
        Session:SessionDeps
        title: string
            記事のタイトル
        body: String
            記事の内容
    return:
        create_status: Json
    """
    pass


@article.post('/update')
async def update_aricle(Session:SessionDeps, article_data):
    """
    既存の記事を修正するための機能
    args: 
        Session:SessionDeps
        article_data
            記事の情報。modelにて内容は定義
    return:
        update_status: Json

    """
    pass


@article.post('/delete')
async def delete_article(Session: SessionDeps, id):
    """
    既存の記事を削除するための機能
    args: 
        Session:SessionDeps
        id: UUID
            削除する記事のID
    return:
        delete_status: Json
    """
    pass
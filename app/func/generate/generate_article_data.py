from uuid import uuid4
import zlib
from datetime import datetime

from app.models.user.article_models import Article
from app.core.setting import setting


def generate_article_data(
    **kwargs: dict
    ):
    """
    ArticleをDBへインサート可能な形で新たに生成するための関数。
    args:
        **kwargs:
        
        title: str
        記事のタイトル情報を指定。
        
        
        body: str
        記事のコンテンツ情報を指定。
        
        
        user_id: uuid
        ユーザーのUUID情報
        
        
        creaeted_at: datetime
        記事の作成日。デフォルトは現在時刻
        
        
        updated_at: datetime
        記事の更新日。デフォルトは現在時刻
        
        
        is_public: optional[bool]
        記事の公開設定。公開する場合はTrueを選択。
        デフォルトは現在時刻
    """
    article: Article = Article.model_validate(
        {
            'id': uuid4(),
            'title': kwargs.get('title').encode('utf-8'),
            'body': zlib.compress(kwargs.get('body').encode('utf-8')),
            'creaeted_at': kwargs.get('creaeted_at', datetime.now(setting.TZ)),
            'updated_at': kwargs.get('updated_at', datetime.now(setting.TZ)),
            'is_public': kwargs.get('is_public', False),
            'user_id': kwargs.get('user_id')
        }
    )
    return article
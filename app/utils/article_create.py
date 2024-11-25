from uuid import uuid4
from datetime import datetime
import zlib

from app.core.setting import setting
from app.models.user.article_models import Article, SchemaArticleInput


def create_article_params(input_article_params: SchemaArticleInput) -> Article:
    """
    DBへ格納する記事データのエンコード、バリデーション、整形を行う。
    """
    article: Article = Article.model_validate(
        {
            "id": uuid4(),
            "created_at": datetime.now(setting.TZ),
            "updated_at": datetime.now(setting.TZ),
            "title": input_article_params.title.encode('utf-8'),
            'body': zlib.compress(input_article_params.body.encode('utf-8'))
        }
    )
    return create_article_params
import re

from app.models.Article import Article
from app.models.User import User


def parse_search_condition(
    filters_str: list
) -> tuple:
    """
    filters: list
        検索条件をまとめた文字列のリスト
        ['username:=user1', 'or', 'created_at:>2025/05/12']
    return:
        filters: list
    """
    filters = []
    is_and_condition = True
    for filter_str in filters_str:
        # orが入っていた場合の処理
        if filter_str == 'or':
            is_and_condition = False
            continue
        # 文字列のみが入っている場合の処理
        elif not ':' in filter_str:
            filters.append(Article.title.like(f'%{search_str}%'))
            filters.append(Article.body.like(f'%{search_str}%'))
            continue
        
        column_str = filter_str.split(':')[0]
        search_str = filter_str.split(':')[1]
        is_user_filter = hasattr(User, column_str)
        is_artcle_filter = hasattr(Article, column_str)
        # カラムが合致しない場合
        if not is_user_filter and not is_artcle_filter:
            filters.append(Article.title.like(f'%{search_str}%'))
            filters.append(Article.body.like(f'%{search_str}%'))
            continue
        
        # 明示的な検索条件が設定されている場合の処理
        """
        確認内容
            - どの形式の検索条件か。正規表現でチェック
            - どのモデルに対する処理か
            - どのカラムに対する検索条件か。
            - search_strの整形
        """
        model = User if is_user_filter else Article
        
        if re.match('=.*', search_str):
            filters.append(getattr(model, column_str) == search_str[1:])
        elif re.match('>=.*', search_str):
            filters.append(getattr(model, column_str) >= search_str[1:])
        elif re.match('<=.*', search_str):
            filters.append(getattr(model, column_str) <= search_str[1:])
        elif re.match('>.*', search_str):
            filters.append(getattr(model, column_str) > search_str[1:])
        elif re.match('<.*', search_str):
            filters.append(getattr(model, column_str) < search_str[1:])
        elif re.match('!.*', search_str):
            filters.append(getattr(model, column_str) != search_str[1:])
        elif re.match(r'^\[.+,.+\]$', search_str):
            start = search_str[1:-1].split(',')[0]
            end = search_str[1:-1].split(',')[1]
            filters.append(getattr(model, column_str).between(start, end))
        else:
            filters.append(getattr(model, column_str).like(f'%{search_str}%'))
    return is_and_condition, filters

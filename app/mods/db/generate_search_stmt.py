from sqlmodel import select, or_


def generate_search_stmt(
    model, 
    is_and_condition:bool=True, 
    requirements: list | None = None, 
    offset:int | None = None, 
    limit: int | None=None
    )->object:
    """
    DBのselect文を作成する関数
    limit, offset
    
    Args:
        model: model
            UserやArticles等のテーブルを作成しているモデル。
            
        is_and_search: bool = True
            Trueの場合and検索
            Falseの場合or検索
            
        requirements: list | None = None
            フィルタリング条件をリスト形式で記述する。
            == : 等しい
            != : 異なる
            <  : より大きい
            >  : より小さい
            <= : 以上
            >= : 以下
            like: 部分一致
            startswith: 先頭一致
            between: 範囲指定
            in_(): リストに含まれるか。
            ex) 
                1)特定のユーザー名の検索
                    filters = [User.username == '検索したいユーザー名']
                2)特定の日付以前に作成されたユーザー情報
                    filters = [User.create_at < datetime(2025, 03, 01)]
                3)特定の範囲で作成されたユーザー情報
                    filters = [User.create_at.between(datetime(2024, 1, 1), datetime(2025, 3, 1))]
                4)特定の文字列を含む場合
                    filters = [User.username.like(f'%{特定の文字列}%')]
                5)特定の文字列から始まる場合
                    filters = [User.username.startswith('特定の文字列')]
        offset: int | None = None
            指定した数以降の値を返す。
        limt: int | None = None
            指定した数まで返す。
            ex)
                1)該当データの10番目以降を取得
                    offset = 10
                2)該当データの10~20を取得
                    offset = 10, limit =20

    Return:
        stmst: obj
            stmt objectを返す。
    """
    
    if requirements is None:
        stmt = select(model)
    elif is_and_condition:
        stmt = select(model).where(*requirements)
    else: 
        stmt = select(model).where(or_(*requirements))

    if offset is None and limit is None:
        return stmt
    elif isinstance(offset, int) and limit is None:
        stmt = stmt.offset(offset=offset)
    elif offset is None and isinstance(limit, int):
        stmt = stmt.limit(limit=limit)
    elif isinstance(offset, int) and isinstance(limit, int) and offset < limit:
        stmt = stmt.offset(offset=offset).limit(limit=limit)

    return stmt
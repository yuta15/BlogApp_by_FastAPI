from sqlmodel import select, or_


def create_stmt(
    model, 
    method:bool=True, 
    filters: list | None=None, 
    offset:int | None = None, 
    limit: int | None=None
    )->list:
    """
    DBのselect文を作成する関数
    limit, offset
    
    Args:
        model: model
            UserやArticles等のテーブルを作成しているモデル。
        method: bool = True
            defaultはTrue.
            Trueの場合and検索
            Falseの場合or検索
        filters: list | None = None
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
                
    return:
        stmst: any
            stmtを返す。
    """
    stmt = None
    
    if filters is None:
        stmt = select(model)
    else:
        stmt = select(model).where(*filters) if method else select(model).where(or_(*filters))

    if offset is None and limit:
        stmt = stmt.limit(limit=limit)
    elif offset and limit is None:
        stmt = stmt.offset(offset=offset)
    elif offset and limit:
        if offset > limit:
            return stmt
        stmt = stmt.offset(offset=offset).limit(limit=limit)

    return stmt
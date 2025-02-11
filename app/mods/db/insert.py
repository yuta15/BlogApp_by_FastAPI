from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError


def insert_data(
    *,
    session: Session,
    data: any
    ) -> bool:
    """
    DBへデータをinsertする関数

    Args:
        session (Session): SQLAlchemyのDBセッション
        data (Any): 挿入するデータ（SQLModelまたはSQLAlchemy Model）

    Returns:
        bool: 成功時はTrue

    Raises:
        OperationalError: データベースの接続エラーやタイムアウト
        IntegrityError: データの重複などの制約違反
        Exception: その他の予期しないエラー
    """
    try:
        session.add(data)
        session.commit()
    except (OperationalError, IntegrityError):
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    return True
from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError


def delete_data(
    *,
    session: Session,
    data: any
    ) -> bool:
    """
    DBへデータをdeleteする関数

    Args:
        session (Session): SQLAlchemyのDBセッション
        data (Any): deleteするデータ（SQLModelまたはSQLAlchemy Model）

    Returns:
        bool: 成功時はTrue

    Raises:
        OperationalError: データベースの接続エラーやタイムアウト
        IntegrityError: データの重複などの制約違反
        Exception: その他の予期しないエラー
    """
    try:
        session.delete(data)
        session.commit()
    except (OperationalError, IntegrityError):
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    return True
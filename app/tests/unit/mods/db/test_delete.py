import pytest


def delete_user(db_session, inserted_user):
    """
    ユーザー削除機能のテスト
    """
    session = db_session
    user = inserted_user
    
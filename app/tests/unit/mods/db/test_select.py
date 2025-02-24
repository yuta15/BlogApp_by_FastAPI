import pytest
from sqlmodel import select

from app.mods.db.select import select_data
from app.models.User import User



def test_select_user(db_session, create_users, insert_data_fixture):
    """select_dataのテスト"""
    user_count = 4
    session = db_session
    users = create_users(number = user_count)
    for user in users:
        insert_data_fixture(session, user)
        assert user == select_data(session=session, stmts=select(User).where(User.username == user.username))[0]
        assert user == select_data(session=session, stmts=select(User).where(User.email == user.email))[0]
        assert user == select_data(session=session, stmts=select(User).where(User.uuid == user.uuid))[0]
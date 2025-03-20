import pytest
from sqlmodel import select
from datetime import datetime

from app.mods.db.select_data import select_data
from app.models.User import User
from app.models.Article import Article


def test_select_user(db_session, create_users, insert_data_fixture):
    """select_dataのテスト"""
    user_count = 4
    session = db_session
    users = create_users(number = user_count)
    for user in users:
        insert_data_fixture(session, user)
        assert user == select_data(session=session, stmt=select(User).where(User.username == user.username))[0]
        assert user == select_data(session=session, stmt=select(User).where(User.email == user.email))[0]
        assert user == select_data(session=session, stmt=select(User).where(User.uuid == user.uuid))[0]


def test_select_some_stmt(db_session, create_users, insert_data_fixture):
    """様々なフィルタリング条件での検索を実施"""
    user_count = 4
    session = db_session
    users = create_users(number=user_count)
    for user in users:
        user.username = f'select_partial_match_stmt{users.index(user)}'
        user.create_at = datetime(2022, 1, 1, 12, 0, 0)
        user.update_at = datetime(2024, 1, 1, 12, 0, 0)
        insert_data_fixture(session=session, data=user)
    stmt1 = select(User).where(User.username.like(f'%partial%')).order_by(User.username)
    stmt2 = select(User).where(User.username.startswith('select_')).order_by(User.username)
    stmt3 = select(User).where(User.create_at < datetime(2024, 1, 1, 12, 0, 0)).order_by(User.username)
    stmt4 = select(User).where(User.create_at.between(datetime(2021, 1, 1, 12, 0, 0), datetime(2024, 1, 1, 12, 0, 0))).order_by(User.username)
    assert users == select_data(session=session, stmt=stmt1)
    assert users == select_data(session=session, stmt=stmt2)
    assert users == select_data(session=session, stmt=stmt3)
    assert users == select_data(session=session, stmt=stmt4)
    
    
def test_select_stmt_offset_2(db_session, create_users, insert_data_fixture):
    """様々なフィルタリング条件での検索を実施"""
    user_count = 4
    session = db_session
    users = create_users(number=user_count)
    currect_user = []
    # print(users)
    for user in users:
        user.username = f'select_stmt_offset_2_{users.index(user)}'
        user.create_at = datetime(2022, 1, 1, 12, 0, 0)
        user.update_at = datetime(2024, 1, 1, 12, 0, 0)
        if users.index(user) == 2 or users.index(user) == 3:
            currect_user.append(user.model_copy())
        insert_data_fixture(session=session, data=user) 
    stmt1 = select(User).where(User.username.like(f'%offset_2%')).order_by(User.username).offset(2)
    stmt2 = select(User).where(User.username.startswith('select_stmt_offset')).order_by(User.username).offset(2)
    assert currect_user == select_data(session=session, stmt=stmt1)
    assert currect_user == select_data(session=session, stmt=stmt2)


def test_select_articles(db_session, create_users, create_articles, insert_data_fixture):
    """select_dataのテスト"""
    user_count = 4
    session = db_session
    users = create_users(number=user_count)
    for user in users:
        insert_data_fixture(session=session, data=user)
        article = create_articles(user_id=user.uuid)[0]
        insert_data_fixture(session=session, data=article)
        assert article == select_data(session=session, stmt=select(Article).where(Article.id == article.id))[0]

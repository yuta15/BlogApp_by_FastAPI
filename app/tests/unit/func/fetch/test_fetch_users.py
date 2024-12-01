import pytest

from app.models.user.user_models import User
from app.tests.mods import get_db

from app.func.fetch.fetch_users import fetch_users



@pytest.mark.parametrize(
    [
        'user_params',
        'search_val',
        'result',
    ],
    [
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            {'username': 'testuser'},
            True
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            {'email': 'testuser@example.com'},
            True
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            {'username': 'testuser', 'email': 'testuser@example.com'},
            True
        ),
    ]
)
def test_fetch_user_success(
    generate_user,
    user_params,
    search_val,
    result,
):
    """
    fetch_userのテスト用関数
    """
    session = next(get_db.get_db())
    user = generate_user(user_params)
    user.insert_user(session=session)

    users = fetch_users(
        session=session, 
        table_model=User, 
        **search_val
        )
    if result:
        assert users == [user.user]
    user.delete_user(session=session)


@pytest.mark.parametrize(
    [
        'user_params',
    ],
    [
        pytest.param(
            {'username': 'testuser2', 'password': 'testuser2', 'email': 'testuser2@example.com'},
        )
    ]
)
def test_fetch_user_success_by_uuid(
    generate_user,
    user_params
):
    """
    fetch_userのテスト用関数。UUIDによってデータを取得するためのテスト
    """
    session = next(get_db.get_db())
    
    user = generate_user(user_params)
    user.insert_user(session=session)
    search_val = {'uuid': user.uuid}
    users = fetch_users(
        session = session,
        table_model = User,
        **search_val
    )
    
    assert users == [user.user]
    user.delete_user(session=session)

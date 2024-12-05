import pytest

from app.models.user.user_models import User
from app.tests.mods import get_db
from app.func.fetch.fetch_users import fetch_users


@pytest.mark.parametrize(
    [
        'user_params',
        'search_keys',
        'is_and_search',
        'result',
    ],
    [
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            ['username'],
            True,
            True
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            ['email'],
            False,
            True
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            ['uuid'],
            True,
            True
        ),
    ]
)
def test_fetch_users(
    user_params,
    search_keys,
    is_and_search,
    result,
    user_fixture
):
    user = user_fixture(user_params)
    session = next(get_db.get_db())
    user.insert_user(session=session)
    search_params = {}
    for key in search_keys:
        if key == 'username':
            search_params[key] = user.username
        if key == 'email':
            search_params[key] = user.email
        if key == 'uuid':
            search_params[key] = user.uuid

    if is_and_search:
        users = fetch_users(
            session=session,
            table_model=User,
            **search_params
        )
    else:
        users = fetch_users(
            session=session,
            condition='or',
            table_model=User,
            **search_params
        )
    if result:
        assert users == [user.user]
    
    user.delete_user(session=session)
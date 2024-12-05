import pytest
from sqlalchemy.exc import DBAPIError, OperationalError, IntegrityError

from app.tests.mods.get_db import get_db
from app.func.insert.insert_user import insert_user

@pytest.mark.parametrize(
    [
        'user_params',
        'result'
    ],
    [
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            None
        ),
        pytest.param(
            {'username': 'user1', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            'IntegrityError'
        ),
    ]
)
def test_insert_user(
    user_params,
    result,
    user_fixture
):
    """
    insert_userのテスト用関数
    """
    
    session = next(get_db())
    user = user_fixture(user_params)
    inser_user_params = user.user
    return_val = insert_user(session=session, user=inser_user_params)
    if not result:
        assert return_val == result
    else:
        assert return_val.get('Error') == result
    
    
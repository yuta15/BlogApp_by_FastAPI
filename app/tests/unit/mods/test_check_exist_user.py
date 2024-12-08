import pytest
from fastapi.exceptions import HTTPException

from app.mods.user import check_exist_user
from app.tests.mods.get_db import get_db
from app.models.user.user_models import User

@pytest.mark.parametrize(
    [
        'user_params',
        'mock_return_val',
        'result',
        'status_code'
    ],
    [
        pytest.param(
            {'username': 'testuser', 'email': 'tesetuser@example.com', 'password': 'testuserpassword'},
            [],
            True,
            None
        ),
        pytest.param(
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'user1password'},
            [],     ## Falseの場合はこのリスト内にデータを追加する。
            False,
            409
        )
    ]
)
def test_check_exist_user(
    user_fixture,
    monkeypatch,
    user_params,
    mock_return_val,
    result,
    status_code
):
    
    user = user_fixture(user_params)
    if not result:
        mock_return_val.append(user.user)
    fake_input_user = user.input_user
    session = next(get_db())
    monkeypatch.setattr(check_exist_user, 'fetch_users', lambda session=session, table_model=User, condition='or', username=user.username, email=user.email: mock_return_val)
    if result:
        return_val = check_exist_user.check_exist_user(session=session, user_input=fake_input_user)
        assert return_val == None
    else:
        with pytest.raises(
            HTTPException
        ) as e:
            check_exist_user.check_exist_user(session=session, user_input=fake_input_user)
        assert e.value.status_code == status_code
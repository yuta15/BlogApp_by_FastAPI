import pytest
from fastapi.exceptions import HTTPException


from app.mods._user import auth_user


@pytest.mark.parametrize(
    [
        'user_params',
        'result',
        'status_code'
    ],
    [
        pytest.param(
            {'username': 'testuser', 'email': 'tesetuser@example.com', 'password': 'testuserpassword'},
            True,
            None
        ),
        pytest.param(
            {'username': 'testuser', 'email': 'tesetuser@example.com', 'password': 'testuserpassword'},
            False,
            400
        )
    ]
)
def test_auth_user(
    user_params,
    result,
    status_code,
    user_fixture,
    monkeypatch
):
    user = user_fixture(user_params)
    monkeypatch.setattr(auth_user.check_password, 'check_password', lambda input_password=user.password, user=user: result)
    if result:
        auth_user.auth_user(input_password=user.password, user=user)
    else:
        with pytest.raises(HTTPException) as e:
            auth_user.auth_user(input_password=user.password, user=user)
        assert e.value.status_code == status_code
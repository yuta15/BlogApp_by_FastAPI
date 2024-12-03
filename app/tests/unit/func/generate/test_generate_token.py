import pytest
from datetime import datetime, timedelta, timezone

from app.func.generate.generate_token import generate_token


@pytest.mark.parametrize(
    [
        'user_params',
        'iat',
        'time_delta',
        'subject'
    ],
    [
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            datetime.now(tz=timezone(timedelta(hours=+9))),
            timedelta(hours=+9),
            {'username': 'testuser', 'email': 'testuser@example.com'}
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            datetime.now(tz=timezone(timedelta(hours=+9))),
            timedelta(hours=-9),
            {'username': 'testuser', 'email': 'testuser@example.com'}
        ),
    ]
)
def test_generate_token(
    user_params, iat, time_delta, subject, user_fixture
):
    """
    Tokenの値を検証するための関数
    """
    user = user_fixture(user_params)
    payload = user.generate_payload(iat=iat, time_delta=time_delta, subject=subject)
    token = user.generate_token(payload=payload)
    generated_token = generate_token(payload=payload)
    
    assert token == generated_token
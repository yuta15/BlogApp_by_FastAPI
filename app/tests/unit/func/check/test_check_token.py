import pytest
from datetime import datetime, timedelta, timezone
from jwt.exceptions import (
    ExpiredSignatureError, 
    InvalidSignatureError, 
    DecodeError,
    )

from app.core.setting import setting
from app.func.check.check_token import check_token


@pytest.mark.parametrize(
    [
        'user_params',
        'extension',
        'iat',
        'time_delta',
        'secret_key',
        'result_message'
    ],
    [
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            None,
            datetime.now(tz=timezone(timedelta(hours=+9))),
            timedelta(minutes=+15),
            setting.SECRET_KEY,
            None
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            ExpiredSignatureError,
            datetime.now(tz=timezone(timedelta(hours=+9))),
            timedelta(minutes=-15),
            setting.SECRET_KEY,
            'Signature has expired'
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            ExpiredSignatureError,
            datetime.now(tz=timezone(timedelta(hours=+9))),
            timedelta(minutes=-15),
            'test_secret',
            'Signature verification failed'
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            DecodeError,
            datetime.now(tz=timezone(timedelta(hours=+9))),
            timedelta(minutes=+15),
            setting.SECRET_KEY,
            'Not enough segments'
        ),
    ]
)
def test_check_token(
    user_params,
    extension,
    iat,
    time_delta,
    secret_key,
    result_message,
    user_fixture
):
    user = user_fixture(user_params)
    subject = {'username': user.username, 'email': user.email}
    payload = user.generate_payload(iat=iat, time_delta=time_delta, subject=subject)
    token = user.generate_token(payload=payload, secret_key=secret_key)
    if extension == DecodeError:
        token = token[:len(token)//2]
    if extension is None:
        assert check_token(token) == subject
    else:
        with pytest.raises(
            (
                ExpiredSignatureError,
                InvalidSignatureError,
                DecodeError
            )
        ) as e:
            check_token(token)
        assert str(e.value) == result_message
from fastapi import HTTPException
import pytest
from datetime import timedelta
from datetime import datetime, timedelta, timezone
from jwt.exceptions import (
    ExpiredSignatureError, 
    InvalidSignatureError, 
    DecodeError,
    InvalidTokenError
    )

from app.tests.mods.generate_payload import generate_payload
from app.tests.mods.generate_token import generate_token


from app.func.check.check_token import check_token


@pytest.mark.parametrize(
    [
        'username',
        'email',
        'delta',
    ],
    [
        pytest.param(
            'user1',
            'use1@example.com',
            timedelta(minutes=15),
        )
    ]
)
def test_check_token_success(username, email, delta):
    """
    
    """
    payload = generate_payload(
        username, 
        email, 
        datetime.now(timezone(timedelta(hours=+9))), 
        delta
        )
    token = generate_token(payload=payload)
    assert check_token(token) == payload.get('sub')
    
    
    
@pytest.mark.parametrize(
    [
        'ext',
        'iat',
        'delta',
        'secret_key',
        'result',
    ],
    [
        pytest.param(
            ExpiredSignatureError,
            datetime.now(timezone(timedelta(hours=+9))),
            timedelta(minutes=-15),
            'dev-secret-key',
            'Signature has expired'
        ),
        pytest.param(
            InvalidSignatureError,
            datetime.now(timezone(timedelta(hours=+9))),
            timedelta(minutes=15),
            'test_secret',
            'Signature verification failed'
        ),
        pytest.param(
            DecodeError,
            datetime.now(timezone(timedelta(hours=+9)))+timedelta(days=+15),
            timedelta(minutes=-15),
            'dev-secret-key',
            'Not enough segments'
        )
    ]
)
def test_check_token_failed(ext, iat, delta, secret_key, result):
    """
    
    """
    username = 'user1'
    email = 'user1@example.com'
    payload = generate_payload(
        username=username,
        email=email,
        iat=iat,
        time_delta=delta)
    token = generate_token(payload=payload, secret_key=secret_key)
    
    if ext == DecodeError:
        token = ''
    
    with pytest.raises(
        (
            ExpiredSignatureError,
            InvalidSignatureError,
            DecodeError,
        )
        ) as e:
        check_token(token)
    assert str(e.value) == result

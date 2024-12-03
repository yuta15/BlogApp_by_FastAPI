import pytest
from datetime import datetime, timedelta, timezone

from app.func.generate.generate_payload import generate_payload


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
        )
    ]
)
def test_generate_payload(
    user_params,
    iat,
    time_delta,
    subject,
    user_fixture
):
    user = user_fixture(user_params)
    user_arg = user.user
    payload = user.generate_payload(iat = iat, time_delta=time_delta, subject=subject)
    generated_paylod = generate_payload(user_arg)
    assert payload.get('sub') == generated_paylod.get('sub')
import pytest

from app.core.setting import pwd_context
from app.func.generate.generate_hash_password import generate_hash_password


@pytest.mark.parametrize(
    [
        'plain_password',
    ],
    [
        pytest.param(
            'testuserpassword'
        )
    ]
)
def test_generate_hash_password(
    plain_password
):
    """
    hashパスワードを比較する。
    """
    hashed_password = generate_hash_password(plain_password=plain_password)
    is_availble = pwd_context.verify(plain_password, hashed_password)
    assert is_availble == True
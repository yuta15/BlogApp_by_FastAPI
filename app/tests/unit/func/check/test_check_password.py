import pytest

from app.tests.mods.generate_hashed_password import generate_hashed_password
from app.func.check.check_password import check_password

@pytest.mark.parametrize(
    [
        'password',
        'hashed_password',
        'return_bool'
    ],
    [
        pytest.param(
            'user1password',
            None,
            False
        ),
        pytest.param(
            'user2password',
            generate_hashed_password('user2password'),
            True
        ),
    ]
)
def test_check_password(password, hashed_password, return_bool):
    """
    ハッシュパスワードはすべてuser1passwordのもの
    """
    is_ckecked = check_password(plain_password=password, hashed_password=hashed_password)
    assert is_ckecked == return_bool
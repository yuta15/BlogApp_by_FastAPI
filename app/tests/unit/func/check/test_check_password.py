import pytest

from app.func.check.check_password import check_password

@pytest.mark.parametrize(
    [
        'user_params',
        'is_valid'
    ],
    [
        pytest.param(
            {'username':'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            True
        ),
        pytest.param(
            {'username':'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            False
        ),
    ]
)
def test_check_password(user_params, is_valid, user_fixture):
    """
    ハッシュパスワードはすべてuser1passwordのもの
    """
    user = user_fixture(user_params)
    password = user.password
    hashed_password = user.hashed_password
    if not is_valid:
        password = 'testFailedPassword'
    is_ckecked = check_password(plain_password=password, hashed_password=hashed_password)
    assert is_ckecked == is_valid
import pytest

from app.func.generate.generate_user import generate_user


@pytest.mark.parametrize(
    [
        'user_params',
        'is_success'
    ],
    [
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            True
        ),
        pytest.param(
            {'username': 'testuser', 'password': 'testuserpassword', 'email': 'testuser@example.com'},
            False
        ),
    ]
)
def test_generate_user(
    user_params,
    is_success,
    user_fixture
):
    user = user_fixture(user_params)
    if not is_success:
        replaced_email = user.email.replace('@', '')
        with pytest.raises(ValueError) as e:
            target_user = generate_user(
                username = user.username,
                hashed_password = user.hashed_password,
                email = replaced_email
            )
        assert str(e.value) == 'Validation Error!!!'
        
    else:
        target_user = generate_user(
            username = user.username,
            hashed_password = user.hashed_password,
            email = user.email
        )
        assert target_user.username == user.username
        assert target_user.email == user.email
    
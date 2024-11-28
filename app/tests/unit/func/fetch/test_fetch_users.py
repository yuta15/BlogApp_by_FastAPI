import pytest
from pytest_mock import MockerFixture, MockFixture

from app.models.user.user_models import User
from app.tests.mods import fetch_user_data, get_db

def test_fetch_user_success(
    mocker: MockerFixture
):
    """
    
    """
    session = get_db.get_db()
    user: User = fetch_user_data.fetch_user(session=session)[0]
    
    mock_db = mocker.pathc()
import pytest

from app.tests.mods.get_db import create_table
from app.tests.mods.FakeUser import FakeUser


@pytest.fixture(scope='function')
def user_fixture():
    """
    疑似的なUserデータを生成するための関数
    """
    create_table()
    def _generate_user(user_params):
        return FakeUser(user_params)
        
    return _generate_user

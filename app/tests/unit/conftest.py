import pytest
from app.tests.mods.FakeUser import FakeUser


@pytest.fixture(scope='function')
def generate_user():
    """
    疑似的なUserデータを生成するための関数
    """
    def _generate_user(user_params):
        return FakeUser(user_params)
        
    return _generate_user

import pytest

from app.core.db import get_db
from app.tests.unit.test_mods.create_user import create_success_users



@pytest.fixture(scope='module')
def db_session():
    """
    sessionを作成するfixture
    """
    session = get_db()
    yield session
    
    
@pytest.fixture(scope='module')
def create_users():
    """
    insertするユーザー情報を作成する
    """
    def _create_users(
        number: int = 1, 
        is_only_admin_user: bool = False,
        is_only_normal_user: bool = False,
        is_only_active_user: bool = False,
        is_only_inactive_user: bool = False
    ):
        users = create_success_users(number=3, is_active_users=False, is_admin_users=True)
        return users


@pytest.fixture(scope='module')
def create_article():
    """
    insertするarticleデータを作成する。
    """
    users = create_success_users(is_active_users=True)
    

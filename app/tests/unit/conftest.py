import pytest
from uuid import UUID

from app.core.db import get_db
from app.tests.unit.test_mods.create_user import create_success_users
from app.tests.unit.test_mods.create_articles import create_success_articles
from app.tests.unit.test_mods.insert_test_data import insert_test_data


@pytest.fixture(scope='function')
def db_session():
    """
    sessionを作成するfixture
    """
    session = next(get_db())
    yield session
    session.close()
    
    
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
        users = create_success_users(
            number=number, 
            is_only_admin_user=is_only_admin_user, 
            is_only_normal_user=is_only_normal_user, 
            is_only_active_user=is_only_active_user, 
            is_only_inactive_user=is_only_inactive_user
            )
        return users
    
    return _create_users


@pytest.fixture(scope='function')
def create_articles():
    """
    insertするarticleデータを作成する。
    """
    def _create_articles(
        user_id: UUID,
        number: int = 1,
        is_only_public: bool = False,
    ):
        articles = create_success_articles(
            user_id=user_id,
            number=number,
            is_only_public=is_only_public
        )
        return articles
    
    return _create_articles


@pytest.fixture(scope='function')
def insert_data_fixture():
    def _insert_test_user(session, data):
        insert_test_data(session=session, data=data)
    return _insert_test_user
import pytest
from sqlmodel import SQLModel

from app.tests.mods.get_db import engin
from app.models.user.user_models import User
from app.models.user.article_models import Article
from app.models.superuser.superuser import Superuser


@pytest.fixture()
def init_db():
    SQLModel.metadata.create_all(engin)
import pytest
from fastapi.testclient import TestClient
from typing import List

from app.main import app
from app.test.utils.db import db_init
from app.test.utils.token import create_token_headers


@pytest.fixture(scope='session', autouse=True)
def init_db():
    db_init()
    yield
    db_init()
    
    
@pytest.fixture(scope='module')
def client():
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope='module')
def token_header() -> List[dict]:
    headers = create_token_headers()
    return headers
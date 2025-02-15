import pytest
import os

from app.core.db import create_table, drop_table
from app.lifespan.init_db import init_db


@pytest.fixture(scope='session', autouse=True)
def db_init():
    """
    DBを初期化する為のfixture
    """
    os.environ['Env'] = 'Testing'
    
    create_table()
    
    yield
    
    drop_table()
    create_table()
    init_db()
    os.environ['Env'] = 'Dev'
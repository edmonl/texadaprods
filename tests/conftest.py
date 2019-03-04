import os
import tempfile

import pytest

import api


@pytest.fixture
def app():
    db_file, db_path = tempfile.mkstemp()
    app = api.create_app({'TESTING': True, 'DATABASE': db_path})

    with app.app_context(), open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
        api.db.init_db()
        with api.db.cursor() as cur:
            cur.executescript(f.read().decode('utf8'))

    yield app
    os.close(db_file)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()

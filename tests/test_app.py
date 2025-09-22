import os
import tempfile
import pytest
from app import app, db
from models import Task

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_create_task(client):
    rv = client.post('/tasks', data={'title':'Teste'}, follow_redirects=True)
    assert b'Teste' in rv.data

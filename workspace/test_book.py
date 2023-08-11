import pytest

from app import app, db, Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

def test_get_all_books(client):
    book = Book(title='testbook', author='testauthor', year='2000', summary='testsummary')
    db.session.add(book)
    db.session.commit()

    response = client.get('/api/book')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['title'] == 'testbook'

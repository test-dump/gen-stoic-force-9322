import pytest

from app import app, db, User, Book, Review

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

def test_add_review(client):
    user = User(username='testuser', password=User.encrypt_password('password'))
    db.session.add(user)

    book = Book(title='testbook', author='testauthor', year='2000', summary='testsummary')
    db.session.add(book)
    db.session.commit()

    review = Review(rating=5, text='Great book!', user_id=user.id, book_id=book.id)
    db.session.add(review)
    db.session.commit()

    response = client.get(f'/api/review/{book.id}')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['rating'] == 5
    assert data[0]['text'] == 'Great book!'

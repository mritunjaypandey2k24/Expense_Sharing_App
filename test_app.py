import pytest
from app import create_app
from models import db, User, Expense, Split

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_user(client):
    response = client.post('/user', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'mobile': '1234567890'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_add_expense(client):
    # First, create a user
    client.post('/user', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'mobile': '1234567890'
    })

    # Then, add an expense
    response = client.post('/expense', json={
        'amount': 100,
        'description': 'Test Expense',
        'split_method': 'equal',
        'user_id': 1,
        'splits': [
            {'user_id': 1, 'amount': 50},
            {'user_id': 2, 'amount': 50}
        ]
    })
    assert response.status_code == 201
    assert b'Expense added successfully' in response.data

def test_get_balance_sheet(client):
    # Add a user and an expense first
    client.post('/user', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'mobile': '1234567890'
    })
    client.post('/expense', json={
        'amount': 100,
        'description': 'Test Expense',
        'split_method': 'equal',
        'user_id': 1,
        'splits': [
            {'user_id': 1, 'amount': 50},
            {'user_id': 2, 'amount': 50}
        ]
    })

    response = client.get('/balance_sheet')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert b'User ID,Name,Balance' in response.data

# Add more tests as needed
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
load_dotenv('/home/menelikberhan/REST-API_for_Ethiopic_Script_OCR/tests/test_env')
from pymongo import MongoClient
import json

@pytest.fixture
def client():
    test_db_client = MongoClient("localhost", 27017)
    test_db = test_db_client.test_db
    test_db.drop_collection("users")
    from api.v1.app import app
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def user(client):
    response = client.post("/user/register", json={"username": "test", "password": "test", 'email': 'test@a.com'})
    assert response.status_code == 201
    user = response.json()
    return {"username": "test", "password": "test", 'email': 'test@a.com'}


@pytest.fixture
def token(client):
    response = client.post("/user/register", json={"username": "test", "password": "test", 'email': 'test@a.com'})
    assert response.status_code == 201
    user = response.json()
    # Login
    response = client.post("/user/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    return headers

def test_register_user(client):
    response = client.post("/user/register", json={"username": "test_user", "password": "test", 'email': 'test_user@example.com'})

    # Check that the response is successful
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "test_user@example.com"
    # add more assertions based on your user model

def test_login_user(client, user):
    response = client.post("/user/login", data={"username": user['username'], "password": user['username']})

    # Check that the response is successful
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_current_user(client, token):
 
    # Make request to the API
    response = client.get("/user/me/", headers=token)

    # Check that the response is successful
    assert response.status_code == 200
    assert "username" in response.json()
    assert response.json()["username"] == "test"
    assert response.json()["email"] == "test@a.com"
    assert 'id' in response.json()

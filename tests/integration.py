import pytest
from fastapi.testclient import TestClient
from asyncio import get_event_loop
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv('/home/menelikberhan/REST-API_for_Ethiopic_Script_OCR/a/test_env')
# from db.mongodb import db_client
from api.v1.app import app


@pytest.fixture()
def client():
    test_db_client = MongoClient("localhost", 27017)
    test_db = test_db_client.test_db
    test_db.drop_collection("users")
    # from api.v1.app import app
    with TestClient(app) as test_client:
        yield test_client
    

def test_app_flow(client):

    # Create user
    response = client.post("/user/register", json={"username": "test", "password": "test", 'email': 'test@a.com'})
    assert response.status_code == 201
    user = response.json()
    # Login
    response = client.post("/user/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Upload image
    with open("amh-test.png", "rb") as f:
        response = client.post("/image", files={"file": f}, headers=headers)
    assert response.status_code == 201
    image_id = response.json()["id"]

    # Get image OCR result
    response = client.get(f"/ocr/image/{image_id}", params={"format": "str", "add_format": False}, headers=headers)
    assert response.status_code == 200

    # Upload PDF
    with open("amh-test.pdf", "rb") as f:
        response = client.post("/pdf", files={"file": f}, headers=headers)
    assert response.status_code == 201
    pdf_id = response.json()["id"]

    # Get PDF OCR result
    response = client.get(f"/ocr/pdf/{pdf_id}", params={"format": "str", "add_format": False}, headers=headers)
    assert response.status_code == 200
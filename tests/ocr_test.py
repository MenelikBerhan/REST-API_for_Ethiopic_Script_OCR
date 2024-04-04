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
def headers(client):
    response = client.post("/user/register", json={"username": "test", "password": "test", 'email': 'test@a.com'})
    assert response.status_code == 201
    user = response.json()
    # Login
    response = client.post("/user/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    return headers

@pytest.fixture
def image_id(client, headers):
    files = {
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }
    response = client.post("/image/", files=files, headers=headers)
    return response.json().get('id')

@pytest.fixture
def pdf_id(client, headers):
    files = {
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }
    response = client.post("/pdf/", files=files, headers=headers)
    return response.json().get('id')

@pytest.fixture
def image_id_txt(client, headers):
    files = {
        "image_properties": (None, json.dumps({"ocr_output_formats": ["str", "txt"]}), 'application/json'),
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }
    response = client.post("/image/", files=files, headers=headers)
    return response.json().get('id')

@pytest.fixture
def pdf_id_txt(client, headers):
    files = {
        "pdf_properties": (None, json.dumps({"ocr_output_formats": ["str", "txt"]}), 'application/json'),
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }
    response = client.post("/pdf/", files=files, headers=headers)
    return response.json().get('id')

@pytest.fixture
def image_id_docx(client, headers):
    files = {
        "image_properties": (None, json.dumps({"ocr_output_formats": ["str", "docx"]}), 'application/json'),
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }
    response = client.post("/image/", files=files, headers=headers)
    return response.json().get('id')

@pytest.fixture
def pdf_id_docx(client, headers):
    files = {
        "pdf_properties": (None, json.dumps({"ocr_output_formats": ["str", "docx"]}), 'application/json'),
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }
    response = client.post("/pdf/", files=files, headers=headers)
    return response.json().get('id')


def test_get_image_ocr_output_file_formats(client, headers, image_id, image_id_txt, image_id_docx):
    response = client.get(f"/ocr/image/done/{image_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["str"]

    response = client.get(f"/ocr/image/done/{image_id_txt}", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["str", "txt"]

    response = client.get(f"/ocr/image/done/{image_id_docx}", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["str", "docx"]


def test_get_pdf_ocr_output_file_formats(client, headers, pdf_id, pdf_id_txt, pdf_id_docx):
    response = client.get(f"/ocr/pdf/done/{pdf_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["str"]

    response = client.get(f"/ocr/pdf/done/{pdf_id_txt}", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["str", "txt"]

    response = client.get(f"/ocr/pdf/done/{pdf_id_docx}", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["str", "docx"]




# def test_get_image_ocr_result(client):
#     # Replace with actual image_id, user, format and add_format
#     image_id = "test_image_id"
#     user = "test_user"
#     format = "str"
#     add_format = False
#     response = client.get(f"/ocr/image/{image_id}", params={"format": format, "add_format": add_format}, headers={"user": user})
#     assert response.status_code == 200

# def test_get_pdf_ocr_result(client):
#     # Replace with actual pdf_id, user, format and add_format
#     pdf_id = "test_pdf_id"
#     user = "test_user"
#     format = "str"
#     add_format = False
#     response = client.get(f"/ocr/pdf/{pdf_id}", params={"format": format, "add_format": add_format}, headers={"user": user})
#     assert response.status_code == 200
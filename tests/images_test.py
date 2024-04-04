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

def test_create_image(client, headers):
    # Prepare data for the image file
    image_properties = {
        "description": "test image",
        "ocr_output_formats": ["str", "txt"]
    }
    tesseract_config = {
        "config_vars": {
            "load_system_dawg": 0,
            "preserve_interword_spaces": 1
        },
        "language": "amh-old",
        "oem": 1,
        "psm": 3
    }
    files = {
        "image_properties": (None, json.dumps(image_properties), 'application/json'),
        "tesseract_config": (None, json.dumps(tesseract_config), 'application/json'),
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }

    response = client.post("/image/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    image_data = response.json()
    assert "id" in image_data
    assert "ocr_finished" in image_data
    assert image_data["name"] == "amh-test.png"
    assert image_data["description"] == "test image"
    assert image_data['ocr_output_formats'] == ["str", "txt"]

def test_create_image_no_file(client, headers):
    # Prepare data for the image file
    image_properties = {
        "description": "test image",
        "ocr_output_formats": ["str", "txt"]
    }
    tesseract_config = {
        "config_vars": {
            "load_system_dawg": 0,
            "preserve_interword_spaces": 1
        },
        "language": "amh-old",
        "oem": 1,
        "psm": 3
    }
    files = {
        "image_properties": (None, json.dumps(image_properties), 'application/json'),
        "tesseract_config": (None, json.dumps(tesseract_config), 'application/json'),
    }

    response = client.post("/image/", files=files, headers=headers)

    # Check that the response is unsuccessful
    assert response.status_code == 422

def test_create_image_no_tesseract_config(client, headers):
    # Prepare data for the image file
    image_properties = {
        "description": "test image",
        "ocr_output_formats": ["str", "txt", "docx"]
    }
    files = {
        "image_properties": (None, json.dumps(image_properties), 'application/json'),
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }

    response = client.post("/image/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    image_data = response.json()
    assert "id" in image_data
    assert "ocr_finished" in image_data
    assert image_data["name"] == "amh-test.png"
    assert image_data["description"] == "test image"
    assert image_data['ocr_output_formats'] == ["str", "txt", "docx"]


def test_create_image_no_image_properties(client, headers):
    # Prepare data for the image file
    tesseract_config = {
        "config_vars": {
            "load_system_dawg": 0,
            "preserve_interword_spaces": 1
        },
        "language": "amh-old",
        "oem": 1,
        "psm": 3
    }
    files = {
        "tesseract_config": (None, json.dumps(tesseract_config), 'application/json'),
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }

    response = client.post("/image/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    image_data = response.json()
    assert "id" in image_data
    assert "ocr_finished" in image_data
    assert image_data["name"] == "amh-test.png"
    assert image_data["description"] == ""
    assert image_data['ocr_output_formats'] == ["str"]


def test_create_image_file_only(client, headers):
    # Prepare data for the image file
    files = {
        "file": ("amh-test.png", open("amh-test.png", 'rb'), "image/png"),
    }

    response = client.post("/image/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    image_data = response.json()
    assert "id" in image_data
    assert "ocr_finished" in image_data
    assert image_data["name"] == "amh-test.png"
    assert image_data["description"] == ""
    assert image_data['ocr_output_formats'] == ["str"]
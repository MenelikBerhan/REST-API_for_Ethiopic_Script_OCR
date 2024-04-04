import pytest
from fastapi import UploadFile
from dotenv import load_dotenv
from fastapi.testclient import TestClient
load_dotenv('/home/menelikberhan/REST-API_for_Ethiopic_Script_OCR/a/test_env')
# from api.v1.app import app
from io import BytesIO
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

def test_create_pdf(client, headers):
    # Prepare data for the pdf file
    pdf_properties = {
        "description": "test pdf",
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
        "pdf_properties": (None, json.dumps(pdf_properties), 'application/json'),
        "tesseract_config": (None, json.dumps(tesseract_config), 'application/json'),
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }

    response = client.post("/pdf/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    pdf_data = response.json()
    assert "id" in pdf_data
    assert "ocr_finished" in pdf_data
    assert pdf_data["name"] == "amh-test.pdf"
    assert pdf_data["description"] == "test pdf"
    assert pdf_data['ocr_output_formats'] == ["str", "txt"]

def test_create_pdf_no_file(client, headers):
    # Prepare data for the pdf file
    pdf_properties = {
        "description": "test pdf",
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
        "pdf_properties": (None, json.dumps(pdf_properties), 'application/json'),
        "tesseract_config": (None, json.dumps(tesseract_config), 'application/json'),
    }

    response = client.post("/pdf/", files=files, headers=headers)

    # Check that the response is unsuccessful
    assert response.status_code == 422

def test_create_pdf_no_tesseract_config(client, headers):
    # Prepare data for the pdf file
    pdf_properties = {
        "description": "test pdf",
        "ocr_output_formats": ["str", "txt", "docx"]
    }
    files = {
        "pdf_properties": (None, json.dumps(pdf_properties), 'application/json'),
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }

    response = client.post("/pdf/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    pdf_data = response.json()
    assert "id" in pdf_data
    assert "ocr_finished" in pdf_data
    assert pdf_data["name"] == "amh-test.pdf"
    assert pdf_data["description"] == "test pdf"
    assert pdf_data['ocr_output_formats'] == ["str", "txt", "docx"]


def test_create_pdf_no_pdf_properties(client, headers):
    # Prepare data for the pdf file
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
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }

    response = client.post("/pdf/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    pdf_data = response.json()
    assert "id" in pdf_data
    assert "ocr_finished" in pdf_data
    assert pdf_data["name"] == "amh-test.pdf"
    assert pdf_data["description"] == ""
    assert pdf_data['ocr_output_formats'] == ["str"]


def test_create_pdf_file_only(client, headers):
    # Prepare data for the pdf file
    files = {
        "file": ("amh-test.pdf", open("amh-test.pdf", 'rb'), "application/pdf"),
    }

    response = client.post("/pdf/", files=files, headers=headers)

    # Check that the response is successful
    assert response.status_code == 201

    # Check that the response data matches what we expect
    pdf_data = response.json()
    assert "id" in pdf_data
    assert "ocr_finished" in pdf_data
    assert pdf_data["name"] == "amh-test.pdf"
    assert pdf_data["description"] == ""
    assert pdf_data['ocr_output_formats'] == ["str"]

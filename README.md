# __REST-API for Ethiopic Script OCR__

![image](https://github.com/MenelikBerhan/REST-API_for_Ethiopic_Script_OCR/assets/125494245/d504f0bd-2b11-457e-87d2-abe3981c57e5)


A RESTfull Web API service to Menelik's Berhan Ethiopic Script OCR app.

# Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup](#setup)
5. [Endpoints](#endpoints)
6. [Usage](#usage)
7. [Testing](#testing)
8. [Contributing](#contributing) 
9. [Contributors](#contributors) 
10. [License](#license)

## Introduction

Menelik's Berhan (loosely translated as Menelik's light) is a web API for OCR services of image and pdf files containing Ethiopic Script texts.

It uses Google's open source tesseract-ocr engine and provides OCR service for texts printed in Amharic, Ge'ez and Tigrigna.

The API is implemented with the intention of using it in web applications, and the overall structure and abstractions in the app take this into consideration.

*Please note that this OCR application is primarily designed to work with printed text. It may not perform well with handwritten text.*

## Features

- Feature 1
- Feature 2
- Feature 3

## Technologies Used
- [Python](https://www.python.org/) (3.8): The whole app is built with Python.
- [FastApi](https://fastapi.tiangolo.com/) (0.110.0): This is the web framework used.
- [Uvicorn](https://www.uvicorn.org/) (0.29.0): An ASGI web server implementation for Python.
- [MongoDB](https://www.mongodb.com/) (7.0.5): This is the database used.
- [Motor](https://www.mongodb.com/docs/drivers/motor/) (3.3.2): Asynchronous Python driver for MongoDB.
- [Pydantic](https://pydantic.dev/) (2.6.4): Data validation library for Python.
- [python-jose](https://python-jose.readthedocs.io/en/latest/) (3.3.0): A JavaScript Object Signing and Encryption (JOSE) implementation in Python.
- [Passlib](https://passlib.readthedocs.io/en/stable/) (1.7.4): A password hashing library for Python
- [Tesseract](https://tesseract-ocr.github.io/) (5.3.4): This is the OCR engine used.
- [PyTesseract](https://pypi.org/project/pytesseract/) (0.3.10): An OCR tool for Python. It's a wrapper for Tesseract-OCR Engine.
- [Aiofiles](https://pypi.org/project/aiofiles/) (23.2.1): A library for handling asynchronous file I/O.
- [NumPy](https://numpy.org/) (1.24.4): A package for scientific computing with Python.
- [OpenCV-python](https://docs.opencv.org/4.9.0/d6/d00/tutorial_py_root.html)(4.9.0.80): A library for real-time computer vision.
- [Pillow](https://python-pillow.org/) (10.2.0): Adds image processing capabilities to Python.
- [python-docx](https://python-docx.readthedocs.org/en/latest/) (1.1.0): Reads, queries and modifies Microsoft Word 2007/2008 docx files.
- [FPDF2](https://py-pdf.github.io/fpdf2/index.html) (2.7.8): A library to create PDF documents using Python.
- [PDF2Image](https://pdf2image.readthedocs.io/en/latest/index.html) (1.17.0): A Python module that converts PDFs into images.
- [Pytest](https://pytest.org/): This is the testing framework used.

## Setup

__Implemented and Tested on Ubuntu 20.04 with Python 3.8__

#### [Install tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)

```bash
# (optional) for tesseract version 5.* add this repository
sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel

# Reload local package database
sudo apt update

# Install tesseract
sudo apt install -y tesseract-ocr
```

#### [Install MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)

```bash
# Install gnupg and curl if they are not already available
sudo apt-get install gnupg curl

# import the MongoDB public GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Reload local package database
sudo apt-get update

# Install the MongoDB packages
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod

# Enable MongoDB on startup
sudo systemctl enable mongod
```

#### Clone the repo
```bash
git clone https://github.com/MenelikBerhan/REST-API_for_Ethiopic_Script_OCR.git
cd REST-API_for_Ethiopic_Script_OCR
```

#### (Optional) Set up a python virtual environment using venv:
Its recommended to setup a python vertual environment before installing requirements:
```bash
sudo apt install -y python3.8-venv
python3 -m venv .venv
source .venv/bin/activate
```

#### Install required packages using pip:
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

#### (Optional) Set environment variables

Change default app variables by setting values in [app_env](/config/app_env) file.

#### Start the app:
```bash
python -m api.v1.app
```

## Endpoints

### `POST /user/register`

- **Description**: Registers a new user.
- **Headers**:
  - `Content-Type`: application/json
- **Body**:
  - `username`: The username of the user. It must be a string.
  - `email`: The email of the user. It must be a valid email string.
  - `password`: The password of the user. It must be a string.
  - `full_name`: The full name of the user. It is optional and can be a string or null.
- **Returns**: A `201 Created` status code and a JSON object representing the new user. None values are excluded from the response. The response object includes the following fields:
  - `id`: The ID of the user.
  - `username`: The username of the user.
  - `email`: The email of the user.
  - `full_name`: The full name of the user.
  - `created_at`: The creation timestamp of the user.
  - `updated_at`: The last updated timestamp of the user.
- **Error codes**:
  - `422 Unprocessable Entity`: If the request body is not valid or the username/email is already taken.
  - `500 Internal Server Error`: If there is a server error.

### `POST /user/login`

- **Description**: Logs in a user based on username & password.
- **Headers**:
  - `Content-Type`: application/x-www-form-urlencoded
- **Body**:
  - `username`: The username of the user.
  - `password`: The password of the user.
- **Returns**: A `200 OK` status code and a JSON object containing the access token. The response object includes the following fields:
  - `access-token`: The access token string.
  - `token-type`: The type of authentication used for the access token.
- **Error codes**: 
  - `401 Unauthorized`: If the username or password is incorrect.
  - `422 Unprocessable Entity`: If the request body is not valid.
  - `500 Internal Server Error`: If there is a server error.

### `GET /user/me/`

- **Description**: Retrieves the current user's information.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Returns**: A `200 OK` status code and a JSON object representing the current user. None values are excluded from the response. The response object includes the following fields:
  - `id`: The ID of the user.
  - `username`: The username of the user.
  - `email`: The email of the user.
  - `full_name`: The full name of the user.
  - `created_at`: The creation timestamp of the user.
  - `updated_at`: The last updated timestamp of the user.
  
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `500 Internal Server Error`: If there is a server error.

### `GET /image/`

- **Description**: Retrieves a list of all images.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Returns**: A `200 OK` status code and a JSON object representing a list of images. None values are excluded from the response. Each image object includes the following fields:
  - `id`: The ID of the image.
  - `created_at`: The creation timestamp of the image.
  - `updated_at`: The last updated timestamp of the image.
  - `name`: The uploaded image's filename.
  - `description`: Brief description of the image.
  - `image_size`: `(width, height)` of the image in pixels.
  - `image_format`: Type of image file.
  - `image_mode`: Mode of an image that defines the type and depth of a pixel in the image.
  - `tess_config_id`: Id of tesseract configuration used for OCR.
  - `tess_output_id`: Id of tesseract output containing OCR results.
  - `ocr_output_formats`: List of desired OCR output file formats.
  - `ocr_finished`: True if background task performing OCR is finished.
  - `ocr_result_text`: Result of OCR by tesseract in string form.
  - `ocr_accuracy`: Average confidence level of words recognized.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `500 Internal Server Error`: If there is a server error.

### `POST /image/`

- **Description**: Inserts a new image record into the database, saves the image in local storage, and performs OCR in the background.
- **Headers**:
  - `Content-Type`: multipart/form-data
  - `Authentication`: Bearer token for authenticating the user.
- **Parameters**: 
  - `image_properties`: Properties of the image to be created (optional). This is a dictionary (`str`:`str`) of image properties. All fields are optional. It includes:
    - `description`: A brief description of the image.
    - `ocr_output_formats`: A list of desired OCR output file formats. By default, the OCR result is saved in string form. If the result is also to be saved in file, and readily available as a response for `GET /ocr/image/{image_id}/`, one or more of `txt`, `docx` or `pdf` must be passed when posting image. After posting the image use the `GET /ocr/image/{image_id}/` endpoint to get result in any format. String output is included in `GET /image/[{image_id}]` response by default.
      - Allowed values: `str` for `string`, `txt` for `plain text` file, `docx` for `Microsoft Word` file or `pdf` for `Pdf` file.
  - `tesseract_config`: Configuration for Tesseract OCR (optional). This is a dictionary (`str`:`str`) of Tesseract config parameters. All fields are optional. It includes:
    - `language`: Tesseract language model to use for OCR. Default is `amh_old`[^2].
      - Allowed values: `amh` for `amharic`, `tig` for `tigrigna`, `amh-old` for `amharic` from old printing presses, and `eng` for `english`.
    - `oem`: OCR engine mode used by Tesseract. Default is `1`.
    - `psm`: Page segmentation mode used by Tesseract. Default is `3`.
    - `config_vars`: `Key: value` pairs of Tesseract config variables (`CONFIGVAR`). Passed to Tesseract using multiple `-c`.
  - `file`: The image file to be uploaded. Maximum image size should be 178956970 pixels[^1].

  ***Reference for `tesseract_config` fields***
    - [TESSERACT(1) Manual Page](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options)
    - [tesseract_parameters](/utils/default_tesseract_parameters) file for list of configurable tesseract variables to use for `config_vars`.
- **Returns**: A `201 Created` status code and a JSON object representing the new image. None values are excluded from the response. It includes:
    - `id`: The ID of the image.
    - `created_at`: The creation timestamp of the image.
    - `updated_at`: The last updated timestamp of the image.
    - `name`: The uploaded image's filename.
    - `description`: A brief description of the image.
    - `ocr_output_formats`: A list of desired OCR output file formats.
    - `ocr_finished`: A boolean indicating whether the background task performing OCR is finished.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `422 Unprocessable Entity`: If any request parameter is not valid.
  - `500 Internal Server Error`: If there is a server error.

### `GET /pdf/`

- **Description**: Retrieves a list of all PDFs in the database. The response is unpaginated and limited to 50 results.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Returns**: A `200 OK` status code and a JSON object representing a list of pdfs. None values are excluded from the response. Each pdf object includes the following fields:
  - `id`: The unique identifier of the PDF.
  - `created_at`: The date and time when the PDF was created.
  - `updated_at`: The date and time when the PDF was last updated.
  - `name`: The name of the uploaded PDF file.
  - `description`: A brief description of the PDF.
  - `ocr_output_formats`: A list of desired OCR output file formats.
  - `ocr_finished`: A boolean indicating whether the background task performing OCR is finished.
  - `pdf_version`: The Portable Document Format (PDF) version.
  - `no_pages`: The number of pages in the PDF.
  - `file_size`: The size of the PDF file in bytes.
  - `page_size`: The size of the PDF pages in points (1 pts = 1/72 inch).
  - `producer`: The program (software) used to create the PDF.
  - `tess_config_id`: The id of the tesseract configuration used for OCR.
  - `tess_output_id`: The id of the tesseract output containing OCR results.
  - `ocr_accuracy`: The average OCR confidence level for each page in the PDF.
  - `ocr_result_text`: The result of OCR for each page in string form.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `500 Internal Server Error`: If there is a server error.

### `POST /pdf/`

- **Description**: Inserts a new PDF record into the database, saves the PDF in local storage, and performs OCR in the background.
- **Headers**:
  - `Content-Type`: multipart/form-data
  - `Authentication`: Bearer token for authenticating the user.
- **Parameters**: 
  - `pdf_properties`: Properties of the pdf to be created (optional). This is a dictionary (`str`:`str`) of pdf properties. All fields are optional. It includes:
    - `description`: A brief description of the pdf.
    - `ocr_output_formats`: A list of desired OCR output file formats. By default, the OCR result is saved in string form. If the result is also to be saved in file, and readily available as a response for `GET /ocr/pdf/{pdf_id}/`, one or more of `txt`, `docx` or `pdf` must be passed when posting image. After posting the pdf use the `GET /ocr/pdf/{pdf_id}/` endpoint to get result in any format. String output is included in `GET /pdf/[{pdf_id}]` response by default.
      - Allowed values: `str` for `string`, `txt` for `plain text` file, `docx` for `Microsoft Word` file or `pdf` for `Pdf` file.
  - `tesseract_config`: Configuration for Tesseract OCR (optional). This is a dictionary (`str`:`str`) of Tesseract config parameters. All fields are optional. It includes:
    - `language`: Tesseract language model to use for OCR. Default is `amh_old`[^2].
      - Allowed values: `amh` for `amharic`, `tig` for `tigrigna`, `amh-old` for `amharic` from old printing presses, and `eng` for `english`.
    - `oem`: OCR engine mode used by Tesseract. Default is `1`.
    - `psm`: Page segmentation mode used by Tesseract. Default is `3`.
    - `config_vars`: `Key: value` pairs of Tesseract config variables (`CONFIGVAR`). Passed to Tesseract using multiple `-c`.
  - `file`: The PDF file containing images to be OCR'ed. Each page in the pdf should have a maximum size of 178956970 pixels[^1].

  ***Reference for `tesseract_config` fields***
    - [TESSERACT(1) Manual Page](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options)
    - [tesseract_parameters](/utils/default_tesseract_parameters) file for list of configurable tesseract variables to use for `config_vars`.
- **Returns**: A `201 Created` status code and a JSON object representing the new PDF. None values are excluded from the response. It includes:
    - `id`: The ID of the pdf.
    - `created_at`: The creation timestamp of the pdf.
    - `updated_at`: The last updated timestamp of the pdf.
    - `name`: The uploaded pdf's filename.
    - `description`: A brief description of the pdf.
    - `ocr_output_formats`: A list of desired OCR output file formats.
    - `ocr_finished`: A boolean indicating whether the background task performing OCR is finished.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `422 Unprocessable Entity`: If any request parameter is not valid.
  - `500 Internal Server Error`: If there is a server error.

### `GET /ocr/image/done/{image_id}`

- **Description**: Retrieves a list of file formats the OCR result is already saved in for a specific image.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Parameters**: 
  - `image_id`: The ID of the image.
- **Returns**: A `200 OK` status code and a list of file formats the OCR result is already saved in. If the list is *empty*, it means the OCR process is *not finished*.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `422 Unprocessable Entity`: If `image_id` is not a valid `bson.ObjectId` object.
  - `404 Not Found`: If the image is not found.
  - `500 Internal Server Error`: If there is a server error.

### `GET /ocr/pdf/done/{pdf_id}`

- **Description**: Retrieves a list of file formats the OCR result is already saved in for a specific PDF.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Parameters**: 
  - `pdf_id`: The ID of the PDF.
- **Returns**: A `200 OK` status code and a list of file formats the OCR result is already saved in. If the list is *empty*, it means the OCR process is *not finished*.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `422 Unprocessable Entity`: If `pdf_id` is not a valid `bson.ObjectId` object.
  - `404 Not Found`: If the pdf is not found.
  - `500 Internal Server Error`: If there is a server error.

### `GET /ocr/image/{image_id}`

- **Description**: Retrieves the OCR result of a specific image as a string or a file.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Parameters**: 
  - `image_id`: The ID of the image.
  - `format`: The file format of the image's OCR result. Default is `str`.
      - Allowed values: `str` for `string`, `txt` for `plain text` file, `docx` for `Microsoft Word` file or `pdf` for `Pdf` file.
  - `add_format`: If the OCR output is not already saved in the given format, this will save the OCR output in the given format and add it to the list of `ocr_output_formats` field of the image. Default is `False`.
- **Returns**: A `200 OK` status code and the OCR result of the image in the requested format.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `422 Unprocessable Entity`: If `image_id` is not a valid `bson.ObjectId` object or if any request parameter is not valid.
  - `404 Not Found`: If the image is not found or the requested `format` is not in the image's `ocr_output_formats` list and `add_format` is set to `False`.
  - `500 Internal Server Error`: If there is a server error.

### `GET /ocr/pdf/{pdf_id}`

- **Description**: Retrieves the OCR result of a specific PDF as a string or a file.
- **Headers**:
  - `Authentication`: Bearer token for authenticating the user.
- **Parameters**: 
  - `pdf_id`: The ID of the PDF.
  - `format`: The file format of the PDF's OCR result. Default is `str`.
    - Allowed values: `str` for `string`, `txt` for `plain text` file, `docx` for `Microsoft Word` file or `pdf` for `Pdf` file.
  - `add_format`: If the OCR output is not already saved in the given format, this will save the OCR output in the given format and add it to the list of `ocr_output_formats` field of the PDF. Default is `False`.
- **Returns**: A `200 OK` status code and the OCR result of the PDF in the requested format. If the `add_format` parameter is set to `True` and the OCR output is not already saved in the given format, a `201 Created` status code is returned.
- **Error codes**: 
  - `401 Unauthorized`: If the user is not authenticated.
  - `422 Unprocessable Entity`: If `pdf_id` is not a valid `bson.ObjectId` object or if any request parameter is not valid.
  - `404 Not Found`: If the pdf is not found or the requested `format` is not in the pdf's `ocr_output_formats` list and `add_format` is set to `False`.
  - `500 Internal Server Error`: If there is a server error.

## Usage

### Register a User

#### Request

`POST /user/register`

```bash
curl -X 'POST' \
  'http://localhost:8000/user/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "menelik@shoa.live",
  "password": "angolala",
  "username": "menelikBerhan",
  "full_name": "Menelik Berahan z Ethiopia"
}'
```
### Response

```bash
 content-length: 215 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:08:35 GMT 
 server: uvicorn 

 {
  "id": "660f24e4fea54f8bc6eecda7",
  "created_at": "2024-04-04T22:08:36.926180Z",
  "updated_at": "2024-04-04T22:08:36.926191Z",
  "username": "menelikBerhan",
  "email": "menelik@shoa.live",
  "full_name": "Menelik Berahan z Ethiopia"
}
```

### Login a User

#### Request

`POST /user/login`

```bash
curl -X 'POST' \
  'http://localhost:8000/user/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=menelikBerhan&password=angolala&scope=&client_id=&client_secret='
```
### Response

```bash
 content-length: 176 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:11:10 GMT 
 server: uvicorn 

 {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc",
  "token_type": "bearer"
}
```

### Get current User

#### Request

`GET /user/me`

```bash
curl -X 'GET' \
  'http://localhost:8000/user/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
 content-length: 213 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:12:59 GMT 
 server: uvicorn 

 {
  "id": "660f24e4fea54f8bc6eecda7",
  "created_at": "2024-04-04T22:08:36.378000",
  "updated_at": "2024-04-04T22:08:36.378000",
  "username": "menelikBerhan",
  "email": "menelik@shoa.live",
  "full_name": "Menelik Berahan z Ethiopia"
}
```

### Create an Image

#### Request

`POST /image/`

```bash
curl -X 'POST' \
  'http://localhost:8000/image/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image_properties={
  "description": "Sample page from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ]
}' \
  -F 'tesseract_config={
  "config_vars": {
    "load_system_dawg": 0,
    "preserve_interword_spaces": 1
  },
  "language": "amh-old",
  "oem": 1,
  "psm": 3
}' \
  -F 'file=@amh-test.png;type=image/png'
```
### Response

```bash
content-length: 257 
content-type: application/json 
date: Thu,04 Apr 2024 22:15:45 GMT 
server: uvicorn 

{
  "id": "660f2692fea54f8bc6eecda8",
  "created_at": "2024-04-04T22:15:46.293190Z",
  "updated_at": "2024-04-04T22:15:46.293204Z",
  "description": "Sample page from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ],
  "name": "amh-test.png",
  "ocr_finished": false
}
```

### Get List of Images

#### Request

`GET /image/`

```bash
curl -X 'GET' \
  'http://localhost:8000/image/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
 content-length: 1623 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:17:42 GMT 
 server: uvicorn

 {
  "images": [
    {
      "id": "660f2692fea54f8bc6eecda8",
      "created_at": "2024-04-04T22:15:46.293000",
      "updated_at": "2024-04-04T22:15:53.103000",
      "description": "Sample page from amharic-amharic dictionary",
      "ocr_output_formats": [
        "str",
        "txt"
      ],
      "name": "amh-test.png",
      "ocr_finished": true,
      "image_size": [
        644,
        560
      ],
      "image_format": "PNG",
      "image_mode": "RGB",
      "tess_config_id": "660f2693fea54f8bc6eecda9",
      "tess_output_id": "660f2698fea54f8bc6eecdaa",
      "ocr_accuracy": 80.91,
      "ocr_result_text": "\n\nመግቢያ \n\nኸሪ ልጆች! ልጆች! እንጫወት በጣም \nከእንግዲህ ልጅነት ተመልሶ አይመጣም \nልጅነቴ! ልጅነቴ፤ ማርና ወተቴ \n\nልጅህን በሚሔድበት መንገድ ምራው በሸመገለ ጊዜ ከእርሱ ፈቀቅ \nእይልም። ፄ \nመጽሐፈ ምሣሌ 11፡16 \n\n... \n. \n\nዕውቀትን ከአንቀልባ እስከ መቃብር ዘመን ፈልጓት \n\nነብዩ መሐመድ (ሰ.አ.ወ) \n\n.. \n\nልጅህን በቀን አንዴ ግሬፈው:፥ አንተ ምን እንዳጠፋ ባታውቅም \nእሱ ያስታውሰዋል \nየቻይናዎች አባባል \n. \n.የክሱር ሰው ጣዕመ መዓዛ እሰስከ ዓለምዳርቻ ይደርሳል፦ \nገድለ ክርሰቶስ ሰምራ \n,ሕፃናትን በእጆቻችን ልናቅፋቸው ባንችል በልባችን እንተፋቸው፦ \nሪደርስ ዳይጀሰት \n. \nለንፁሃን ሁሉም ነገር ንፁህ ነው› \nየአረቦች ምሣሊ \n.ሥ. \nልጆቻችሁ በእናንተ በኩል መጡ እንጂ ከእናንተ አልወጡ፥ \nካህሊል ጊብራል \n\n "
    }
  ]
}
```

### Get List of Finished OCR Output Formats for an Image

#### Request

`GET /ocr/image/done/{image_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/image/done/660f2692fea54f8bc6eecda8' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 13 
content-type: application/json 
date: Thu,04 Apr 2024 22:19:17 GMT 
server: uvicorn

[
  "str",
  "txt"
]
```

### Get OCR Result of an Image

#### Request in string (str) format

`GET /ocr/image/{image_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/image/660f2692fea54f8bc6eecda8?format=str&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
 content-length: 1165 
 content-type: application/json 
 date: Thu,04 Apr 2024 22:21:02 GMT 
 server: uvicorn

 "\n\nመግቢያ \n\nኸሪ ልጆች! ልጆች! እንጫወት በጣም \nከእንግዲህ ልጅነት ተመልሶ አይመጣም \nልጅነቴ! ልጅነቴ፤ ማርና ወተቴ \n\nልጅህን በሚሔድበት መንገድ ምራው በሸመገለ ጊዜ ከእርሱ ፈቀቅ \nእይልም። ፄ \nመጽሐፈ ምሣሌ 11፡16 \n\n... \n. \n\nዕውቀትን ከአንቀልባ እስከ መቃብር ዘመን ፈልጓት \n\nነብዩ መሐመድ (ሰ.አ.ወ) \n\n.. \n\nልጅህን በቀን አንዴ ግሬፈው:፥ አንተ ምን እንዳጠፋ ባታውቅም \nእሱ ያስታውሰዋል \nየቻይናዎች አባባል \n. \n.የክሱር ሰው ጣዕመ መዓዛ እሰስከ ዓለምዳርቻ ይደርሳል፦ \nገድለ ክርሰቶስ ሰምራ \n,ሕፃናትን በእጆቻችን ልናቅፋቸው ባንችል በልባችን እንተፋቸው፦ \nሪደርስ ዳይጀሰት \n. \nለንፁሃን ሁሉም ነገር ንፁህ ነው› \nየአረቦች ምሣሊ \n.ሥ. \nልጆቻችሁ በእናንተ በኩል መጡ እንጂ ከእናንተ አልወጡ፥ \nካህሊል ጊብራል \n\n "
```

#### Request in plain text file (txt) format

`GET /ocr/image/{image_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/image/660f2692fea54f8bc6eecda8?format=txt&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-disposition: attachment; filename="amh-test_ocr-result.txt" 
content-length: 1127 
content-type: text/plain; charset=utf-8 
date: Thu,04 Apr 2024 22:22:19 GMT 
etag: "aad385818e384e7a3c070bf65d80eea9" 
last-modified: Thu,04 Apr 2024 22:15:53 GMT 
server: uvicorn

መግቢያ 

ኸሪ ልጆች! ልጆች! እንጫወት በጣም 
ከእንግዲህ ልጅነት ተመልሶ አይመጣም 
ልጅነቴ! ልጅነቴ፤ ማርና ወተቴ 

ልጅህን በሚሔድበት መንገድ ምራው በሸመገለ ጊዜ ከእርሱ ፈቀቅ 
እይልም። ፄ 
መጽሐፈ ምሣሌ 11፡16 

... 
. 

ዕውቀትን ከአንቀልባ እስከ መቃብር ዘመን ፈልጓት 

ነብዩ መሐመድ (ሰ.አ.ወ) 

.. 

ልጅህን በቀን አንዴ ግሬፈው:፥ አንተ ምን እንዳጠፋ ባታውቅም 
እሱ ያስታውሰዋል 
የቻይናዎች አባባል 
. 
.የክሱር ሰው ጣዕመ መዓዛ እሰስከ ዓለምዳርቻ ይደርሳል፦ 
ገድለ ክርሰቶስ ሰምራ 
,ሕፃናትን በእጆቻችን ልናቅፋቸው ባንችል በልባችን እንተፋቸው፦ 
ሪደርስ ዳይጀሰት 
. 
ለንፁሃን ሁሉም ነገር ንፁህ ነው› 
የአረቦች ምሣሊ 
.ሥ. 
ልጆቻችሁ በእናንተ በኩል መጡ እንጂ ከእናንተ አልወጡ፥ 
ካህሊል ጊብራል 
```

### Create a PDF

#### Request

`POST /pdf/`

```bash
curl -X 'POST' \
  'http://localhost:8000/pdf/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc' \
  -H 'Content-Type: multipart/form-data' \
  -F 'pdf_properties={
  "description": "Sample pages from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ]
}' \
  -F 'tesseract_config={
  "config_vars": {
    "load_system_dawg": 0,
    "preserve_interword_spaces": 1
  },
  "language": "amh-old",
  "oem": 1,
  "psm": 3
}' \
  -F 'file=@desta.pdf;type=application/pdf'
```
### Response

```bash
content-length: 255 
content-type: application/json 
date: Thu,04 Apr 2024 22:25:24 GMT 
server: uvicorn

{
  "id": "660f28d4fea54f8bc6eecdab",
  "created_at": "2024-04-04T22:25:24.644697Z",
  "updated_at": "2024-04-04T22:25:24.644705Z",
  "description": "Sample pages from amharic-amharic dictionary",
  "ocr_output_formats": [
    "str",
    "txt"
  ],
  "name": "desta.pdf",
  "ocr_finished": false
}
```

### Get List of PDFs

#### Request

`GET /pdf/`

```bash
curl -X 'GET' \
  'http://localhost:8000/pdf/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 10616 
content-type: application/json 
date: Thu,04 Apr 2024 22:26:25 GMT 
server: uvicorn

{
  "pdfs": [
    {
      "id": "660f28d4fea54f8bc6eecdab",
      "created_at": "2024-04-04T22:25:24.644000",
      "updated_at": "2024-04-04T22:26:14.406000",
      "description": "Sample pages from amharic-amharic dictionary",
      "ocr_output_formats": [
        "str",
        "txt"
      ],
      "name": "desta.pdf",
      "ocr_finished": true,
      "pdf_version": "1.7",
      "no_pages": 2,
      "file_size": "676660 bytes",
      "page_size": "841.92 x 1190.52 pts (A3)",
      "producer": "Microsoft: Print To PDF",
      "tess_config_id": "660f2693fea54f8bc6eecda9",
      "tess_output_id": "660f2906fea54f8bc6eecdac",
      "ocr_accuracy": {
        "1": 90.64,
        "2": 89.95
      },
      "ocr_result_text": {
        "1": "\n\nመቅድም ። \n\nፈረንጆች ፡ የኢትዮጵያ ፡ መንበረ ፡ መንግሥት ፡ በጐንደር ፡ ከነበረበት ፡ ዘመን ፡ ም \nረው ፡ በየጊዜው ፡ ያማርኛን ፡ ግስ ፡ እየጸፉ ፡ አሳትመዋል ። ከኹሉ ፡ አስቀድሞ ፡ ባጭሩ ፡ \nጽፎ ፡ ያሳተመው ፡ ሉዶልፍ ፡ ይባላል ። \n\n፪ኛው ፡ ጀርመናዊው ፡ ኢዝንበርግ ፡ ነው ። እሱም ፡ ዐማርኛን ፡ ከትግሪኛ ፡ ሳይለይ ፡ \nደባልቆ ፡ ጽል ፤ ምክንያቱም ፡ በትግሬ ፡ ተቀምጦ ፡ ትግሮችንና ፡ ያማራ ፡ ነጋዶችን ፡ ስለ ፡ \nጠየቀ ፡ ይኾናል ። \n\nቦኛው ፡ አንቷን ፡ ዳባዲ ፡ ነው ፤ እሱም ፡ በጐንደር ፡ ተቀምጦ ፡ የጐንደርንና ፡ የሺዋን ፡ \nየጐዣምን ፡ የትግሬን ፡ ሊቃውንት ፡ እየጠየቀ ፡ የተቻለውን ፡ ያኽል ፡ ከግእዝ ፡፣ እያሰማማ ፡ \nጽፎ ፡ አሳትሞታል ፤ አንዳንድ ፡ ዐረብኛም ፡ አግብቶበታል ። ጐንደር ፡ የኹሉ ፡ መሰብለቢያ ፡ \nመዲና ፡ ስለ ፡ ኾነች ፡ ዛሬ ፡ የማይነገር ፡ ብዙ ፡ ዐማርኛ ፡ ይገኝበታል ። ከኢዝንበርግ ፡ ያንቷን ፡ \nዳባዲ ፡ ይሻላል ። \n\n፪ኛው ፡ አግናጥዮስ ፡ ይዲ ፡ ነው ፤ እሱም ፡ በጣሊያን ፡ ከተማ ፡ በሮማ ፡ ተቀምጦ ፡ \nከኢትዮጵያ ፡ ሊቃውንት ፡ በውቀት ፡ መመሪያ ፡ የኾኑ ፡ አራት ፡ ዐይና ፡ የተባሉ ፡ ታላቁን ፡ \nሊቀ ፡ ሊቃውንት ፡ ያንኮበሩ ፡ መምህር ፡ ክፍሌን ፡ እየጠየቀ ፡ አንዳንድ ፡ ዕብራይስጥና ፡ \nዐረሪብኛም ፡ እየጨመረ ፡ በካህናት ፡ ዐማርኛ ፡ አሳጥሮ ፡ ጽፎታል ። የተረሳ ፡ ስም ፡ የቀድሞ ፡ \nወግና ፡ ታሪክም ፡ ዐልፎ ፡ ዐልፎ ፡ ይገኝበታል ። ዳግመኛም ፡ መምህር ፡ ክፍሌ ፡ የብሉይና ፡ \nየሐዲስ ፡ የሊቃውንት ፡ ያቡ ፡ ሻህር ፡ የመጽሐፈ ፡ መነኮሳት ፡ (ያሆራቱ ፡ ጉባኤ) ፡ አስተማሪ ፡ \nስለ ፡ ነበሩ ፡ የዛሬ ፡ ሰዎች ፡ የማያውቁት ፡ ቋንቋ ፡፣ ተጽፎበታል ። አንቷን ፡ ዳባዲን ፡ በመ \nከተል ፡ እንደ ፡ ሮማይስጥ ፡ ፈደል ፡ የአዐንና ፡ የሀሐኀን ፡ የሠሰን ፡ የጸፀንም ፡ ተራ ፡ አንዳንድ ፡ \nወገን ፡ ከሜድረተጉ ፡ በቀር ፡ የርሱ ፡ ግስ ፡ ወደ ፡ ፊት ፡ ለሚጽፉ ፡ አብነት ፡ ይኾናል ። \n\n፳ኛው ፡ የፈረንሳይ ፡ መነዙሴ ፡ አባ ፡ ቤትማን ፡ ነው ። እሱም ፡ ዐዲስ ፡ አበባ ፡ ተቀምጦ ፡ \nየትግሬን ፡ መነኮሳት ፡ እየጠየቀ ፡ ጽፎታል ፤ ትግሪኛውን ፡ ጐንደርኛ ፤ ጋልኛውን ፡ የሺዋ ፡ \nዐማርኛ ፡ ብሎታል ፤ ብዙ ፡ ጊዜ ፡ የጠየቃቸው ፡ ትግሮችና ፡ ጋሎች ፡ እንደ ፡ ኾኑ ፡ በዚህ ፡ \nይታወቃል ። የርሱ ፡ ግስ ፡ ምንም ፡ ስሕተት ፡ ቢኖርበት ፡ አንቷን ፡ ዳባዲና ፡ ይዲ ፡ ከጸፉት ፡ \nይበዛል ። \n\nባላዋቂ ፡ ቤት ፡ እንግዳ ፡ ናኘበት ፡ እንዲሉ ፤ ባ፤ቿ፻ክ ፡ ዓ ፡ ም ፡ የግእዝን ፡ ሰዋስው ፡ \nያሳተሙ ፡ ሰዎች ፤ አብነት ፡ አሞሌ ፡ ዋልጋ ፡ በጋር ፡ ግድነት ፡ ሐርነት ፤ ወረበበ ፡ ሐንከበ ፡ \nጤበ ፡ መረበ ፡ ማህየበ ፡ ተአወሰ ፡ ተመነሰ ፡ ተርኩሰ ፡ ጳስጠመ ፡ ጳርቁመ ፡ መደሐ ፡ ሰተመ ፡ \nወሰከመ ፡ አረመ ፡ ታኤሰ ፡ እያሉ ፡ ዐማርኛውን ፡ በግእዝ ፡ ቦታ ፡ እንዳገቡትና ፡ ግእዝ ፡ ያል \nኾነውን ፡ ፈጠራ ፡ በብዛት ፡ እንደ ፡ ጨመሩበት ፤ ዐማርኛን ፡ ያሰፋ ፡ መስሎት ፡ ባጅ ፡ አዕማድ ፡ \nየማይገሰሰውን ፡ አንቀጽ ፡ እየገሰሰ ፡ ጽል ፤ ያንዱን ፡ ቃል ፡ ከሌላው ፡ አዛንቆታል ፤ (ደባል \nቆታል) ። ዛተ ፡ ዐዘለ ፡ በማለት ፡ ፈንታ ፡ ዘዘተ ፡ ዘዘለ ፡ እያለ ፡ ልብ ፡ ወለድ ፡ ግስ ፡ ይጽፋል ። \n\nይህም ፡ ይህ ፡ ነው ፤ በዚህ ፡ ላይ ፡ ደግሞ ፡ ከግእዙ ፡ የማይለየውን ፡ የካዕቡንና ፡ የሣልሱን፤ \nየራብዑንና ፡ የኃምሱን ፡ የሳድሱንና ፡ የሳብዑን ፡ ተራ ፡ እንደ ፡ ባለዋየሉ ፡ እንደ ፡ ፈረንጅ ፡ \nግስ ፡ ለያይቶ ፡ ጽፎታል ። ነገር ፡ ግን ፡ ያማርኛ ፡ መዝገበ ፡ ቃላት ፡ ሐሳብ ፡ በልባቸው ፡ የሌለ ፡ \nያገራችን ፡ ካህናት ፡ አይታጡምና ፤ በነሱ ፡ አንጻር ፡ ብዙ ፡ ጊዜ ፡ ሊመሰገን ፡ ይገባዋል ። \n\nበንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ ቋንቋ ፡ ተተርጉሞ ፡ በየጊዜው ፡ የታተመው ፤ ኹለ \nቱን ፡ አዐና ፡ ሦስቱን ፡ ሀሐኀኅ ፡ ኹለቱን ፡ ሠሰ ፡ ኹለቱን ፡ ጸፀ ፡ ለይቶ ፡ ያልጸፈ ፡ ያማርኛ ፡ \nግስ ፡ ጥቅምነቱ ፡ ለውጭ ፡ አገር ፡ ሰዎች ፡ ብቻ ፡ ስለ ፡ ኾነ ፡ ላማሮች ፡ የሚጠቅምና ፡ የሚ \nረባ ፡ ይህን ፡ ዐዲስ ፡ ያማርኛ ፡ ግስ ፡ አውጥተናል ። ",
        "2": "\n\nአ መቅድም ። \n\nየፊደሉም ፡ ተራ፡ አበገጐኹጐ ደጀ ሀ ወዘ ሇሐ ኅጐጠጩየከኩ ኸለ መ \nነኘሠዐፈጸፀቀቁቂረ ሰ ሸ ተቸጴደልፐ ፡ ነው ። \n\nግ ጥም ። \n\nየጌታችን ፡ ዕድሜ ፡ ሰባት ፡ ዓመት ፡ ሲያኸል ፡ \nለመምር ፡ ሰጠችው ፡ እናቱ ፡ ድንግል ። \nመምሩም ፡ ሲያስተምረው ፡ አለው ፡ አሌፍ ፡ በል ፣ \nበታምሪየስ ፡ ተጽጁል ፡ ይህ ፡ ቃል ። \nጌታም ፡ ለመምሩ ፡ ጥያቄ ፡ ሰጠው ፣ \nምስጢረ ፡ ፈጣሪን ፡ ገልጦ ፡ ሊያስረዳው ፡ \nምንት ፡ ትርሳጓሜሁ ፡ ለአሌፍ ፡ አለው ። \nአሌፍ ፡ ስለ ፡ ኾነ ፡ የፊደሎች ፡ በዙር ፡ \nየትም ፡ አገር ፡ የለ ፡ በሀ ፡ መመር ። \nዕብራይስጥና ፡ ዐረብ ፡ ሱርስትም ፡ ይቅሩና ፡ \nበትግሬ ፡ ግዛት ፡ በአቫስም ፡ መዲና ፡ \nየሳባ ፡ ፊደል ፡ ግእዝ ፡ ያባተው ፡ \nበአ ፡ ነበርና ፡ የሚዥምረው 1፤ \nለሀ ፡ መነሻነት ፡ ምሰክር ፡ የለው ፤ \nኦንዲያው ፡ ፈጠራና ፡ ልብ ፡ ወለድም ፡ ነው ። \n\nኢዝንበርግ ፡ በትግሬ ፡ አውራጃ ፡ ሳለ ፡ አበገደን ፡ ከግራ ፡ ወደ ፡ ቀኝ ፡ በደንጊያ ፡ ተቀርጾ ፡ \nስላገኘው ፡ ሥዕሉን ፡ አንሥቶ ፡ በግሱ ፡ ውስጥ ፡ አሳትሞታል ፤ ስለዚህ ፡ አበገደ ፡ ጥንታዊ ፡ \nነው ፡ እንጂ ፤ እንደ ፡ ሀለሐመ ፡ ኋለኛ ፡ አይዶለም ። \n\nባውሮጳ ፡ በየመንግሥታቱ ፡ ኹሉ ፡ ቋንቋን ፡፣ የሚያፋፉና ፡ የሚያስፋፉ ፡ የሚጠብቁ ፡ \nየሚከባከቡ ፡ የቋንቋ ፡ ሞግዚቶች ፡ የተባሉ ፡ ብዙ ፡ ሊቃውንት ፡ አሉ ። \n\nበግብጽም ፡ አገር ፡ ላገር ፡ እየዞሩ ፡ በፈብኛን ፡ የሚማርሩ ፡ ሊቃውንት ፡ ይገኛሉ ። ጉባኤያ \nቸውም ፡ ቤተ ፡ መምህራን ፡ ቤተ ፡ ደራስያን ፡ ይባላል ። ቋንቋቸውም ፡ ከዚህ ፡ የተነሣ ፡ እነሱን ፡ \nጠቅሞ ፡ በውጭ ፡ አገር ፡ ሰፋ ፤ ተንሰራፋ ። ቅብጥንና ፡ ሳባን ፡ የመሰለ ፡ ጥንታዊ ፡ \nልሳን ፡ ከነፊደሉ ፡ ጠፍቶና ፡ ተረስቶ ፡ እንዳይቀር ፡ ከራሳቸው ፡ ቋንቋ ፡ ዐልፈው ፡ ተርፈው ፡ \nየሌላውን ፡ ልሳን ፡፣ ይጠብቃሉ ። ቃልም ፡ ቢጐድልባቸው ፡ ከሌሎች ፡ ቋንቋ ፡ ወስደው ፡ በፊ \nደላቸው ፡ ጽፈው ፡ የራሳቸው ፡ ያደርጉታል ። ከነዚህም ፡ ሊቃውንት ፡ ግእዝንና ፡ ዐማርኛን ፡ \nየሚያውቁ ፡ በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ በመስኮብ ፡ ባሜሪካ ፡ ከተማ ፡ ይገኛሉ ። \nይልቁንም ፡ በጀርመን ፡ አገር ፡ ሥራችን ፡ ብለው ፡ ግእዝንና ፡ ዐማርኛን ፡ ይማራሉ ፤ ያስተ \nምራሉ ። እነደጃዝማች ፡ ተሰማ ፡ ገዝሙንም ፡ ባዩ ፡ ጊዜ ፤ «ደአንትሙ ፡ ትበልዑ ፡ በእዴክሙ ፤ \nንሕነሰ ፡ ንበልዕ ፡ በመንካ» ፡ እያሉ ፡ ይናገራሉ ፤ (ተናገሩ) ። ሠዓሊው ፡ አቶ ፡ አገኘኹ ፡ እንግ \nዳና ፡ አቶ ፡ ታደገ ፡ ከበበውም ፡ በኢትዮጵያ ፡ መንግሥት ፡ ዐልጋ ፡ ወራሽ ፡ ልዑል ፡ ተፈሪ ፡ \nመኩንን ፡ (ዛሬ ፡ ቀዳማዊ ፡ ዐጤ ፡ ኀይለ ፡ ሥላሴ) ፡ ፈቃድ ፡ ፓሪስ ፡ በኺዱ ፡ ጊዜ ፡ ፈረንሳድይኛ ፡ \nእስኪለምዱ ፡ ድረስ ፡ ከፈረንሳይ ፡ ሊቃውንት ፡ ጋራ ፡ በግእዝ ፡ ሲነጋገሩ ፡ እንደ ፡ ቁየና ፡ \nግእዝን ፡ ባገራችን ፡ እኛ ፡ እንዲያ ፡ ስንንቀው ፡ እሱ ፡ በባዕድ ፡ አገር ፡ እንደ ፡ ዮሴፍ ፡ እጅማ ፡ \nበጣም ፡ ጠቀመን ፡ እያሉ ፡ ሲናገሩ ፡ ከቃላቸው ፡ ሰሞቻለኹ ። "
      }
    }
  ]
}
```

### Get List of Finished OCR Output Formats for a PDF

#### Request

`GET /ocr/pdf/{pdf_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/pdf/done/660f28d4fea54f8bc6eecdab' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 13 
content-type: application/json 
date: Thu,04 Apr 2024 22:27:20 GMT 
server: uvicorn

[
  "str",
  "txt"
]
```

### Get OCR Result of a PDF

#### Request in string format

`GET /ocr/pdf/{pdf_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/pdf/660f28d4fea54f8bc6eecdab?format=str&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-length: 10072 
content-type: application/json 
date: Thu,04 Apr 2024 22:28:05 GMT 
server: uvicorn

{
  "1": "\n\nመቅድም ። \n\nፈረንጆች ፡ የኢትዮጵያ ፡ መንበረ ፡ መንግሥት ፡ በጐንደር ፡ ከነበረበት ፡ ዘመን ፡ ም \nረው ፡ በየጊዜው ፡ ያማርኛን ፡ ግስ ፡ እየጸፉ ፡ አሳትመዋል ። ከኹሉ ፡ አስቀድሞ ፡ ባጭሩ ፡ \nጽፎ ፡ ያሳተመው ፡ ሉዶልፍ ፡ ይባላል ። \n\n፪ኛው ፡ ጀርመናዊው ፡ ኢዝንበርግ ፡ ነው ። እሱም ፡ ዐማርኛን ፡ ከትግሪኛ ፡ ሳይለይ ፡ \nደባልቆ ፡ ጽል ፤ ምክንያቱም ፡ በትግሬ ፡ ተቀምጦ ፡ ትግሮችንና ፡ ያማራ ፡ ነጋዶችን ፡ ስለ ፡ \nጠየቀ ፡ ይኾናል ። \n\nቦኛው ፡ አንቷን ፡ ዳባዲ ፡ ነው ፤ እሱም ፡ በጐንደር ፡ ተቀምጦ ፡ የጐንደርንና ፡ የሺዋን ፡ \nየጐዣምን ፡ የትግሬን ፡ ሊቃውንት ፡ እየጠየቀ ፡ የተቻለውን ፡ ያኽል ፡ ከግእዝ ፡፣ እያሰማማ ፡ \nጽፎ ፡ አሳትሞታል ፤ አንዳንድ ፡ ዐረብኛም ፡ አግብቶበታል ። ጐንደር ፡ የኹሉ ፡ መሰብለቢያ ፡ \nመዲና ፡ ስለ ፡ ኾነች ፡ ዛሬ ፡ የማይነገር ፡ ብዙ ፡ ዐማርኛ ፡ ይገኝበታል ። ከኢዝንበርግ ፡ ያንቷን ፡ \nዳባዲ ፡ ይሻላል ። \n\n፪ኛው ፡ አግናጥዮስ ፡ ይዲ ፡ ነው ፤ እሱም ፡ በጣሊያን ፡ ከተማ ፡ በሮማ ፡ ተቀምጦ ፡ \nከኢትዮጵያ ፡ ሊቃውንት ፡ በውቀት ፡ መመሪያ ፡ የኾኑ ፡ አራት ፡ ዐይና ፡ የተባሉ ፡ ታላቁን ፡ \nሊቀ ፡ ሊቃውንት ፡ ያንኮበሩ ፡ መምህር ፡ ክፍሌን ፡ እየጠየቀ ፡ አንዳንድ ፡ ዕብራይስጥና ፡ \nዐረሪብኛም ፡ እየጨመረ ፡ በካህናት ፡ ዐማርኛ ፡ አሳጥሮ ፡ ጽፎታል ። የተረሳ ፡ ስም ፡ የቀድሞ ፡ \nወግና ፡ ታሪክም ፡ ዐልፎ ፡ ዐልፎ ፡ ይገኝበታል ። ዳግመኛም ፡ መምህር ፡ ክፍሌ ፡ የብሉይና ፡ \nየሐዲስ ፡ የሊቃውንት ፡ ያቡ ፡ ሻህር ፡ የመጽሐፈ ፡ መነኮሳት ፡ (ያሆራቱ ፡ ጉባኤ) ፡ አስተማሪ ፡ \nስለ ፡ ነበሩ ፡ የዛሬ ፡ ሰዎች ፡ የማያውቁት ፡ ቋንቋ ፡፣ ተጽፎበታል ። አንቷን ፡ ዳባዲን ፡ በመ \nከተል ፡ እንደ ፡ ሮማይስጥ ፡ ፈደል ፡ የአዐንና ፡ የሀሐኀን ፡ የሠሰን ፡ የጸፀንም ፡ ተራ ፡ አንዳንድ ፡ \nወገን ፡ ከሜድረተጉ ፡ በቀር ፡ የርሱ ፡ ግስ ፡ ወደ ፡ ፊት ፡ ለሚጽፉ ፡ አብነት ፡ ይኾናል ። \n\n፳ኛው ፡ የፈረንሳይ ፡ መነዙሴ ፡ አባ ፡ ቤትማን ፡ ነው ። እሱም ፡ ዐዲስ ፡ አበባ ፡ ተቀምጦ ፡ \nየትግሬን ፡ መነኮሳት ፡ እየጠየቀ ፡ ጽፎታል ፤ ትግሪኛውን ፡ ጐንደርኛ ፤ ጋልኛውን ፡ የሺዋ ፡ \nዐማርኛ ፡ ብሎታል ፤ ብዙ ፡ ጊዜ ፡ የጠየቃቸው ፡ ትግሮችና ፡ ጋሎች ፡ እንደ ፡ ኾኑ ፡ በዚህ ፡ \nይታወቃል ። የርሱ ፡ ግስ ፡ ምንም ፡ ስሕተት ፡ ቢኖርበት ፡ አንቷን ፡ ዳባዲና ፡ ይዲ ፡ ከጸፉት ፡ \nይበዛል ። \n\nባላዋቂ ፡ ቤት ፡ እንግዳ ፡ ናኘበት ፡ እንዲሉ ፤ ባ፤ቿ፻ክ ፡ ዓ ፡ ም ፡ የግእዝን ፡ ሰዋስው ፡ \nያሳተሙ ፡ ሰዎች ፤ አብነት ፡ አሞሌ ፡ ዋልጋ ፡ በጋር ፡ ግድነት ፡ ሐርነት ፤ ወረበበ ፡ ሐንከበ ፡ \nጤበ ፡ መረበ ፡ ማህየበ ፡ ተአወሰ ፡ ተመነሰ ፡ ተርኩሰ ፡ ጳስጠመ ፡ ጳርቁመ ፡ መደሐ ፡ ሰተመ ፡ \nወሰከመ ፡ አረመ ፡ ታኤሰ ፡ እያሉ ፡ ዐማርኛውን ፡ በግእዝ ፡ ቦታ ፡ እንዳገቡትና ፡ ግእዝ ፡ ያል \nኾነውን ፡ ፈጠራ ፡ በብዛት ፡ እንደ ፡ ጨመሩበት ፤ ዐማርኛን ፡ ያሰፋ ፡ መስሎት ፡ ባጅ ፡ አዕማድ ፡ \nየማይገሰሰውን ፡ አንቀጽ ፡ እየገሰሰ ፡ ጽል ፤ ያንዱን ፡ ቃል ፡ ከሌላው ፡ አዛንቆታል ፤ (ደባል \nቆታል) ። ዛተ ፡ ዐዘለ ፡ በማለት ፡ ፈንታ ፡ ዘዘተ ፡ ዘዘለ ፡ እያለ ፡ ልብ ፡ ወለድ ፡ ግስ ፡ ይጽፋል ። \n\nይህም ፡ ይህ ፡ ነው ፤ በዚህ ፡ ላይ ፡ ደግሞ ፡ ከግእዙ ፡ የማይለየውን ፡ የካዕቡንና ፡ የሣልሱን፤ \nየራብዑንና ፡ የኃምሱን ፡ የሳድሱንና ፡ የሳብዑን ፡ ተራ ፡ እንደ ፡ ባለዋየሉ ፡ እንደ ፡ ፈረንጅ ፡ \nግስ ፡ ለያይቶ ፡ ጽፎታል ። ነገር ፡ ግን ፡ ያማርኛ ፡ መዝገበ ፡ ቃላት ፡ ሐሳብ ፡ በልባቸው ፡ የሌለ ፡ \nያገራችን ፡ ካህናት ፡ አይታጡምና ፤ በነሱ ፡ አንጻር ፡ ብዙ ፡ ጊዜ ፡ ሊመሰገን ፡ ይገባዋል ። \n\nበንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ ቋንቋ ፡ ተተርጉሞ ፡ በየጊዜው ፡ የታተመው ፤ ኹለ \nቱን ፡ አዐና ፡ ሦስቱን ፡ ሀሐኀኅ ፡ ኹለቱን ፡ ሠሰ ፡ ኹለቱን ፡ ጸፀ ፡ ለይቶ ፡ ያልጸፈ ፡ ያማርኛ ፡ \nግስ ፡ ጥቅምነቱ ፡ ለውጭ ፡ አገር ፡ ሰዎች ፡ ብቻ ፡ ስለ ፡ ኾነ ፡ ላማሮች ፡ የሚጠቅምና ፡ የሚ \nረባ ፡ ይህን ፡ ዐዲስ ፡ ያማርኛ ፡ ግስ ፡ አውጥተናል ። ",
  "2": "\n\nአ መቅድም ። \n\nየፊደሉም ፡ ተራ፡ አበገጐኹጐ ደጀ ሀ ወዘ ሇሐ ኅጐጠጩየከኩ ኸለ መ \nነኘሠዐፈጸፀቀቁቂረ ሰ ሸ ተቸጴደልፐ ፡ ነው ። \n\nግ ጥም ። \n\nየጌታችን ፡ ዕድሜ ፡ ሰባት ፡ ዓመት ፡ ሲያኸል ፡ \nለመምር ፡ ሰጠችው ፡ እናቱ ፡ ድንግል ። \nመምሩም ፡ ሲያስተምረው ፡ አለው ፡ አሌፍ ፡ በል ፣ \nበታምሪየስ ፡ ተጽጁል ፡ ይህ ፡ ቃል ። \nጌታም ፡ ለመምሩ ፡ ጥያቄ ፡ ሰጠው ፣ \nምስጢረ ፡ ፈጣሪን ፡ ገልጦ ፡ ሊያስረዳው ፡ \nምንት ፡ ትርሳጓሜሁ ፡ ለአሌፍ ፡ አለው ። \nአሌፍ ፡ ስለ ፡ ኾነ ፡ የፊደሎች ፡ በዙር ፡ \nየትም ፡ አገር ፡ የለ ፡ በሀ ፡ መመር ። \nዕብራይስጥና ፡ ዐረብ ፡ ሱርስትም ፡ ይቅሩና ፡ \nበትግሬ ፡ ግዛት ፡ በአቫስም ፡ መዲና ፡ \nየሳባ ፡ ፊደል ፡ ግእዝ ፡ ያባተው ፡ \nበአ ፡ ነበርና ፡ የሚዥምረው 1፤ \nለሀ ፡ መነሻነት ፡ ምሰክር ፡ የለው ፤ \nኦንዲያው ፡ ፈጠራና ፡ ልብ ፡ ወለድም ፡ ነው ። \n\nኢዝንበርግ ፡ በትግሬ ፡ አውራጃ ፡ ሳለ ፡ አበገደን ፡ ከግራ ፡ ወደ ፡ ቀኝ ፡ በደንጊያ ፡ ተቀርጾ ፡ \nስላገኘው ፡ ሥዕሉን ፡ አንሥቶ ፡ በግሱ ፡ ውስጥ ፡ አሳትሞታል ፤ ስለዚህ ፡ አበገደ ፡ ጥንታዊ ፡ \nነው ፡ እንጂ ፤ እንደ ፡ ሀለሐመ ፡ ኋለኛ ፡ አይዶለም ። \n\nባውሮጳ ፡ በየመንግሥታቱ ፡ ኹሉ ፡ ቋንቋን ፡፣ የሚያፋፉና ፡ የሚያስፋፉ ፡ የሚጠብቁ ፡ \nየሚከባከቡ ፡ የቋንቋ ፡ ሞግዚቶች ፡ የተባሉ ፡ ብዙ ፡ ሊቃውንት ፡ አሉ ። \n\nበግብጽም ፡ አገር ፡ ላገር ፡ እየዞሩ ፡ በፈብኛን ፡ የሚማርሩ ፡ ሊቃውንት ፡ ይገኛሉ ። ጉባኤያ \nቸውም ፡ ቤተ ፡ መምህራን ፡ ቤተ ፡ ደራስያን ፡ ይባላል ። ቋንቋቸውም ፡ ከዚህ ፡ የተነሣ ፡ እነሱን ፡ \nጠቅሞ ፡ በውጭ ፡ አገር ፡ ሰፋ ፤ ተንሰራፋ ። ቅብጥንና ፡ ሳባን ፡ የመሰለ ፡ ጥንታዊ ፡ \nልሳን ፡ ከነፊደሉ ፡ ጠፍቶና ፡ ተረስቶ ፡ እንዳይቀር ፡ ከራሳቸው ፡ ቋንቋ ፡ ዐልፈው ፡ ተርፈው ፡ \nየሌላውን ፡ ልሳን ፡፣ ይጠብቃሉ ። ቃልም ፡ ቢጐድልባቸው ፡ ከሌሎች ፡ ቋንቋ ፡ ወስደው ፡ በፊ \nደላቸው ፡ ጽፈው ፡ የራሳቸው ፡ ያደርጉታል ። ከነዚህም ፡ ሊቃውንት ፡ ግእዝንና ፡ ዐማርኛን ፡ \nየሚያውቁ ፡ በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ በመስኮብ ፡ ባሜሪካ ፡ ከተማ ፡ ይገኛሉ ። \nይልቁንም ፡ በጀርመን ፡ አገር ፡ ሥራችን ፡ ብለው ፡ ግእዝንና ፡ ዐማርኛን ፡ ይማራሉ ፤ ያስተ \nምራሉ ። እነደጃዝማች ፡ ተሰማ ፡ ገዝሙንም ፡ ባዩ ፡ ጊዜ ፤ «ደአንትሙ ፡ ትበልዑ ፡ በእዴክሙ ፤ \nንሕነሰ ፡ ንበልዕ ፡ በመንካ» ፡ እያሉ ፡ ይናገራሉ ፤ (ተናገሩ) ። ሠዓሊው ፡ አቶ ፡ አገኘኹ ፡ እንግ \nዳና ፡ አቶ ፡ ታደገ ፡ ከበበውም ፡ በኢትዮጵያ ፡ መንግሥት ፡ ዐልጋ ፡ ወራሽ ፡ ልዑል ፡ ተፈሪ ፡ \nመኩንን ፡ (ዛሬ ፡ ቀዳማዊ ፡ ዐጤ ፡ ኀይለ ፡ ሥላሴ) ፡ ፈቃድ ፡ ፓሪስ ፡ በኺዱ ፡ ጊዜ ፡ ፈረንሳድይኛ ፡ \nእስኪለምዱ ፡ ድረስ ፡ ከፈረንሳይ ፡ ሊቃውንት ፡ ጋራ ፡ በግእዝ ፡ ሲነጋገሩ ፡ እንደ ፡ ቁየና ፡ \nግእዝን ፡ ባገራችን ፡ እኛ ፡ እንዲያ ፡ ስንንቀው ፡ እሱ ፡ በባዕድ ፡ አገር ፡ እንደ ፡ ዮሴፍ ፡ እጅማ ፡ \nበጣም ፡ ጠቀመን ፡ እያሉ ፡ ሲናገሩ ፡ ከቃላቸው ፡ ሰሞቻለኹ ። "
}
```

#### Request in plain text file (txt) format

`GET /ocr/pdf/{pdf_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/ocr/pdf/660f28d4fea54f8bc6eecdab?format=txt&add_format=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZW5lbGlrQmVyaGFuIiwiZXhwIjoxNzEyMjcwNTUyfQ.5WNgV0mOzqi68hJ7t8Ay4XYnP9tphzQZcOM9DI3qjvc'
```
### Response

```bash
content-disposition: attachment; filename="desta_ocr-result.txt" 
content-length: 10005 
content-type: text/plain; charset=utf-8 
date: Thu,04 Apr 2024 22:29:21 GMT 
etag: "6e38d051831dd5d56e08affbf486422f" 
last-modified: Thu,04 Apr 2024 22:26:14 GMT 
server: uvicorn 


መቅድም ። 

ፈረንጆች ፡ የኢትዮጵያ ፡ መንበረ ፡ መንግሥት ፡ በጐንደር ፡ ከነበረበት ፡ ዘመን ፡ ም 
ረው ፡ በየጊዜው ፡ ያማርኛን ፡ ግስ ፡ እየጸፉ ፡ አሳትመዋል ። ከኹሉ ፡ አስቀድሞ ፡ ባጭሩ ፡ 
ጽፎ ፡ ያሳተመው ፡ ሉዶልፍ ፡ ይባላል ። 

፪ኛው ፡ ጀርመናዊው ፡ ኢዝንበርግ ፡ ነው ። እሱም ፡ ዐማርኛን ፡ ከትግሪኛ ፡ ሳይለይ ፡ 
ደባልቆ ፡ ጽል ፤ ምክንያቱም ፡ በትግሬ ፡ ተቀምጦ ፡ ትግሮችንና ፡ ያማራ ፡ ነጋዶችን ፡ ስለ ፡ 
ጠየቀ ፡ ይኾናል ። 

ቦኛው ፡ አንቷን ፡ ዳባዲ ፡ ነው ፤ እሱም ፡ በጐንደር ፡ ተቀምጦ ፡ የጐንደርንና ፡ የሺዋን ፡ 
የጐዣምን ፡ የትግሬን ፡ ሊቃውንት ፡ እየጠየቀ ፡ የተቻለውን ፡ ያኽል ፡ ከግእዝ ፡፣ እያሰማማ ፡ 
ጽፎ ፡ አሳትሞታል ፤ አንዳንድ ፡ ዐረብኛም ፡ አግብቶበታል ። ጐንደር ፡ የኹሉ ፡ መሰብለቢያ ፡ 
መዲና ፡ ስለ ፡ ኾነች ፡ ዛሬ ፡ የማይነገር ፡ ብዙ ፡ ዐማርኛ ፡ ይገኝበታል ። ከኢዝንበርግ ፡ ያንቷን ፡ 
ዳባዲ ፡ ይሻላል ። 

፪ኛው ፡ አግናጥዮስ ፡ ይዲ ፡ ነው ፤ እሱም ፡ በጣሊያን ፡ ከተማ ፡ በሮማ ፡ ተቀምጦ ፡ 
ከኢትዮጵያ ፡ ሊቃውንት ፡ በውቀት ፡ መመሪያ ፡ የኾኑ ፡ አራት ፡ ዐይና ፡ የተባሉ ፡ ታላቁን ፡ 
ሊቀ ፡ ሊቃውንት ፡ ያንኮበሩ ፡ መምህር ፡ ክፍሌን ፡ እየጠየቀ ፡ አንዳንድ ፡ ዕብራይስጥና ፡ 
ዐረሪብኛም ፡ እየጨመረ ፡ በካህናት ፡ ዐማርኛ ፡ አሳጥሮ ፡ ጽፎታል ። የተረሳ ፡ ስም ፡ የቀድሞ ፡ 
ወግና ፡ ታሪክም ፡ ዐልፎ ፡ ዐልፎ ፡ ይገኝበታል ። ዳግመኛም ፡ መምህር ፡ ክፍሌ ፡ የብሉይና ፡ 
የሐዲስ ፡ የሊቃውንት ፡ ያቡ ፡ ሻህር ፡ የመጽሐፈ ፡ መነኮሳት ፡ (ያሆራቱ ፡ ጉባኤ) ፡ አስተማሪ ፡ 
ስለ ፡ ነበሩ ፡ የዛሬ ፡ ሰዎች ፡ የማያውቁት ፡ ቋንቋ ፡፣ ተጽፎበታል ። አንቷን ፡ ዳባዲን ፡ በመ 
ከተል ፡ እንደ ፡ ሮማይስጥ ፡ ፈደል ፡ የአዐንና ፡ የሀሐኀን ፡ የሠሰን ፡ የጸፀንም ፡ ተራ ፡ አንዳንድ ፡ 
ወገን ፡ ከሜድረተጉ ፡ በቀር ፡ የርሱ ፡ ግስ ፡ ወደ ፡ ፊት ፡ ለሚጽፉ ፡ አብነት ፡ ይኾናል ። 

፳ኛው ፡ የፈረንሳይ ፡ መነዙሴ ፡ አባ ፡ ቤትማን ፡ ነው ። እሱም ፡ ዐዲስ ፡ አበባ ፡ ተቀምጦ ፡ 
የትግሬን ፡ መነኮሳት ፡ እየጠየቀ ፡ ጽፎታል ፤ ትግሪኛውን ፡ ጐንደርኛ ፤ ጋልኛውን ፡ የሺዋ ፡ 
ዐማርኛ ፡ ብሎታል ፤ ብዙ ፡ ጊዜ ፡ የጠየቃቸው ፡ ትግሮችና ፡ ጋሎች ፡ እንደ ፡ ኾኑ ፡ በዚህ ፡ 
ይታወቃል ። የርሱ ፡ ግስ ፡ ምንም ፡ ስሕተት ፡ ቢኖርበት ፡ አንቷን ፡ ዳባዲና ፡ ይዲ ፡ ከጸፉት ፡ 
ይበዛል ። 

ባላዋቂ ፡ ቤት ፡ እንግዳ ፡ ናኘበት ፡ እንዲሉ ፤ ባ፤ቿ፻ክ ፡ ዓ ፡ ም ፡ የግእዝን ፡ ሰዋስው ፡ 
ያሳተሙ ፡ ሰዎች ፤ አብነት ፡ አሞሌ ፡ ዋልጋ ፡ በጋር ፡ ግድነት ፡ ሐርነት ፤ ወረበበ ፡ ሐንከበ ፡ 
ጤበ ፡ መረበ ፡ ማህየበ ፡ ተአወሰ ፡ ተመነሰ ፡ ተርኩሰ ፡ ጳስጠመ ፡ ጳርቁመ ፡ መደሐ ፡ ሰተመ ፡ 
ወሰከመ ፡ አረመ ፡ ታኤሰ ፡ እያሉ ፡ ዐማርኛውን ፡ በግእዝ ፡ ቦታ ፡ እንዳገቡትና ፡ ግእዝ ፡ ያል 
ኾነውን ፡ ፈጠራ ፡ በብዛት ፡ እንደ ፡ ጨመሩበት ፤ ዐማርኛን ፡ ያሰፋ ፡ መስሎት ፡ ባጅ ፡ አዕማድ ፡ 
የማይገሰሰውን ፡ አንቀጽ ፡ እየገሰሰ ፡ ጽል ፤ ያንዱን ፡ ቃል ፡ ከሌላው ፡ አዛንቆታል ፤ (ደባል 
ቆታል) ። ዛተ ፡ ዐዘለ ፡ በማለት ፡ ፈንታ ፡ ዘዘተ ፡ ዘዘለ ፡ እያለ ፡ ልብ ፡ ወለድ ፡ ግስ ፡ ይጽፋል ። 

ይህም ፡ ይህ ፡ ነው ፤ በዚህ ፡ ላይ ፡ ደግሞ ፡ ከግእዙ ፡ የማይለየውን ፡ የካዕቡንና ፡ የሣልሱን፤ 
የራብዑንና ፡ የኃምሱን ፡ የሳድሱንና ፡ የሳብዑን ፡ ተራ ፡ እንደ ፡ ባለዋየሉ ፡ እንደ ፡ ፈረንጅ ፡ 
ግስ ፡ ለያይቶ ፡ ጽፎታል ። ነገር ፡ ግን ፡ ያማርኛ ፡ መዝገበ ፡ ቃላት ፡ ሐሳብ ፡ በልባቸው ፡ የሌለ ፡ 
ያገራችን ፡ ካህናት ፡ አይታጡምና ፤ በነሱ ፡ አንጻር ፡ ብዙ ፡ ጊዜ ፡ ሊመሰገን ፡ ይገባዋል ። 

በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ ቋንቋ ፡ ተተርጉሞ ፡ በየጊዜው ፡ የታተመው ፤ ኹለ 
ቱን ፡ አዐና ፡ ሦስቱን ፡ ሀሐኀኅ ፡ ኹለቱን ፡ ሠሰ ፡ ኹለቱን ፡ ጸፀ ፡ ለይቶ ፡ ያልጸፈ ፡ ያማርኛ ፡ 
ግስ ፡ ጥቅምነቱ ፡ ለውጭ ፡ አገር ፡ ሰዎች ፡ ብቻ ፡ ስለ ፡ ኾነ ፡ ላማሮች ፡ የሚጠቅምና ፡ የሚ 
ረባ ፡ ይህን ፡ ዐዲስ ፡ ያማርኛ ፡ ግስ ፡ አውጥተናል ። 
					--- Page 1 ---


አ መቅድም ። 

የፊደሉም ፡ ተራ፡ አበገጐኹጐ ደጀ ሀ ወዘ ሇሐ ኅጐጠጩየከኩ ኸለ መ 
ነኘሠዐፈጸፀቀቁቂረ ሰ ሸ ተቸጴደልፐ ፡ ነው ። 

ግ ጥም ። 

የጌታችን ፡ ዕድሜ ፡ ሰባት ፡ ዓመት ፡ ሲያኸል ፡ 
ለመምር ፡ ሰጠችው ፡ እናቱ ፡ ድንግል ። 
መምሩም ፡ ሲያስተምረው ፡ አለው ፡ አሌፍ ፡ በል ፣ 
በታምሪየስ ፡ ተጽጁል ፡ ይህ ፡ ቃል ። 
ጌታም ፡ ለመምሩ ፡ ጥያቄ ፡ ሰጠው ፣ 
ምስጢረ ፡ ፈጣሪን ፡ ገልጦ ፡ ሊያስረዳው ፡ 
ምንት ፡ ትርሳጓሜሁ ፡ ለአሌፍ ፡ አለው ። 
አሌፍ ፡ ስለ ፡ ኾነ ፡ የፊደሎች ፡ በዙር ፡ 
የትም ፡ አገር ፡ የለ ፡ በሀ ፡ መመር ። 
ዕብራይስጥና ፡ ዐረብ ፡ ሱርስትም ፡ ይቅሩና ፡ 
በትግሬ ፡ ግዛት ፡ በአቫስም ፡ መዲና ፡ 
የሳባ ፡ ፊደል ፡ ግእዝ ፡ ያባተው ፡ 
በአ ፡ ነበርና ፡ የሚዥምረው 1፤ 
ለሀ ፡ መነሻነት ፡ ምሰክር ፡ የለው ፤ 
ኦንዲያው ፡ ፈጠራና ፡ ልብ ፡ ወለድም ፡ ነው ። 

ኢዝንበርግ ፡ በትግሬ ፡ አውራጃ ፡ ሳለ ፡ አበገደን ፡ ከግራ ፡ ወደ ፡ ቀኝ ፡ በደንጊያ ፡ ተቀርጾ ፡ 
ስላገኘው ፡ ሥዕሉን ፡ አንሥቶ ፡ በግሱ ፡ ውስጥ ፡ አሳትሞታል ፤ ስለዚህ ፡ አበገደ ፡ ጥንታዊ ፡ 
ነው ፡ እንጂ ፤ እንደ ፡ ሀለሐመ ፡ ኋለኛ ፡ አይዶለም ። 

ባውሮጳ ፡ በየመንግሥታቱ ፡ ኹሉ ፡ ቋንቋን ፡፣ የሚያፋፉና ፡ የሚያስፋፉ ፡ የሚጠብቁ ፡ 
የሚከባከቡ ፡ የቋንቋ ፡ ሞግዚቶች ፡ የተባሉ ፡ ብዙ ፡ ሊቃውንት ፡ አሉ ። 

በግብጽም ፡ አገር ፡ ላገር ፡ እየዞሩ ፡ በፈብኛን ፡ የሚማርሩ ፡ ሊቃውንት ፡ ይገኛሉ ። ጉባኤያ 
ቸውም ፡ ቤተ ፡ መምህራን ፡ ቤተ ፡ ደራስያን ፡ ይባላል ። ቋንቋቸውም ፡ ከዚህ ፡ የተነሣ ፡ እነሱን ፡ 
ጠቅሞ ፡ በውጭ ፡ አገር ፡ ሰፋ ፤ ተንሰራፋ ። ቅብጥንና ፡ ሳባን ፡ የመሰለ ፡ ጥንታዊ ፡ 
ልሳን ፡ ከነፊደሉ ፡ ጠፍቶና ፡ ተረስቶ ፡ እንዳይቀር ፡ ከራሳቸው ፡ ቋንቋ ፡ ዐልፈው ፡ ተርፈው ፡ 
የሌላውን ፡ ልሳን ፡፣ ይጠብቃሉ ። ቃልም ፡ ቢጐድልባቸው ፡ ከሌሎች ፡ ቋንቋ ፡ ወስደው ፡ በፊ 
ደላቸው ፡ ጽፈው ፡ የራሳቸው ፡ ያደርጉታል ። ከነዚህም ፡ ሊቃውንት ፡ ግእዝንና ፡ ዐማርኛን ፡ 
የሚያውቁ ፡ በንግሊዝ ፡ በፈረንሳይ ፡ በጣሊያን ፡ በመስኮብ ፡ ባሜሪካ ፡ ከተማ ፡ ይገኛሉ ። 
ይልቁንም ፡ በጀርመን ፡ አገር ፡ ሥራችን ፡ ብለው ፡ ግእዝንና ፡ ዐማርኛን ፡ ይማራሉ ፤ ያስተ 
ምራሉ ። እነደጃዝማች ፡ ተሰማ ፡ ገዝሙንም ፡ ባዩ ፡ ጊዜ ፤ «ደአንትሙ ፡ ትበልዑ ፡ በእዴክሙ ፤ 
ንሕነሰ ፡ ንበልዕ ፡ በመንካ» ፡ እያሉ ፡ ይናገራሉ ፤ (ተናገሩ) ። ሠዓሊው ፡ አቶ ፡ አገኘኹ ፡ እንግ 
ዳና ፡ አቶ ፡ ታደገ ፡ ከበበውም ፡ በኢትዮጵያ ፡ መንግሥት ፡ ዐልጋ ፡ ወራሽ ፡ ልዑል ፡ ተፈሪ ፡ 
መኩንን ፡ (ዛሬ ፡ ቀዳማዊ ፡ ዐጤ ፡ ኀይለ ፡ ሥላሴ) ፡ ፈቃድ ፡ ፓሪስ ፡ በኺዱ ፡ ጊዜ ፡ ፈረንሳድይኛ ፡ 
እስኪለምዱ ፡ ድረስ ፡ ከፈረንሳይ ፡ ሊቃውንት ፡ ጋራ ፡ በግእዝ ፡ ሲነጋገሩ ፡ እንደ ፡ ቁየና ፡ 
ግእዝን ፡ ባገራችን ፡ እኛ ፡ እንዲያ ፡ ስንንቀው ፡ እሱ ፡ በባዕድ ፡ አገር ፡ እንደ ፡ ዮሴፍ ፡ እጅማ ፡ 
በጣም ፡ ጠቀመን ፡ እያሉ ፡ ሲናገሩ ፡ ከቃላቸው ፡ ሰሞቻለኹ ። 
					--- Page 2 ---
```

## Testing

#### (Optional) Set testing environment variables

Change testing app variables by setting values in [test_env](/tests/test_env) file.

#### To run the tests, use the following command:
`pytest`

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Contributors

### Girma Eshete aka Menelik Berhan
[Linkedin](https://www.linkedin.com/in/menelikberhan)

## License
[MIT](https://choosealicense.com/licenses/mit/)

[^1]: To avoid: PIL.Image.DecompressionBombError: Image size (... pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack.

[^2]: All language models, except `amh-old`, are from tesseract best language models. `amh-old` is a fine tuned `amh` model using training datas from old amharic printed documents (mostly around the 1950's).

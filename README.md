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
9. [Authors](#authors) 
10. [License](#license)

## Introduction

Menelik's Berhan (loosely translated as Menelik's light) is a web API for OCR services of image and pdf files containing Ethiopic Script texts.

It uses Google's open source tesseract-ocr engine and provides OCR service for texts printed in Amharic, Ge'ez and Tigrigna.

The API is implemented with the intention of using it in web applications, and the overall structure and abstractions in the app take this into consideration.

Concepts learned from previous implementation of [Ethiopic Script CLI OCR app][1] were used for the OCR process.

*Please note that this OCR application is primarily designed to work with printed text. It may not perform well with handwritten text.*

## Features

- **OCR on Images and PDFs**: Perform OCR on images and PDFs containing Ethiopic script text.
- **OCR Process Tracking**: Each OCR process (for image or PDF) is tracked and stored in a database for future analysis.
- **Flexible OCR Outputs**: OCR results can be provided in various formats including plain text, Microsoft Word, and PDF.
- **OCR Result Accuracy**: Provides an accuracy score for OCR results based on the average confidence level of words recognized.
- **Configurable OCR Process**: Users can configure the OCR process by adjusting Tesseract configuration options.
- **Image Preprocessing**: Includes image preprocessing capabilities to improve OCR results.
- **File Storage and Metadata**: Uploaded OCR input image and PDF files are stored locally, with file metadata stored in a database using class abstractions.
- **Fine-Tuned Language Model**: In addition to the default [Tesseract language models][2], includes a fine-tuned model for Amharic, based on texts printed in the 1950s.
- **Data Abstraction for Analysis**: Abstracts input images & PDFs, Tesseract configuration used for OCR, and the OCR process & result using classes, and stores these data in the database for future analysis.
- **OAuth2 User Authentication**: Secure user authentication implemented using FastAPI securities (JWT).

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
- [PDF2Image](https://pdf2image.readthedocs.io/en/latest/index.html) (1.17.0): A Python module that converts PDFs into images.
- [NumPy](https://numpy.org/) (1.24.4): A package for scientific computing with Python.
- [OpenCV-python](https://docs.opencv.org/4.9.0/d6/d00/tutorial_py_root.html)(4.9.0.80): A library for real-time computer vision.
- [Pillow](https://python-pillow.org/) (10.2.0): Adds image processing capabilities to Python.
- [python-docx](https://python-docx.readthedocs.org/en/latest/) (1.1.0): Reads, queries and modifies Microsoft Word 2007/2008 docx files.
- [FPDF2](https://py-pdf.github.io/fpdf2/index.html) (2.7.8): A library to create PDF documents using Python.
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

#### [Install poppler](https://poppler.freedesktop.org/) for [pdf2image](https://pdf2image.readthedocs.io/en/latest/installation.html)
```bash
sudo apt-get -y install poppler-utils
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
- Directly using uvicorn
```bash
python -m api.v1.app
```

- Using gunicorn
```bash
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker api.v1.app:app
```
####

## [Endpoints](/ENDPOINTS.md)

## [Usage](/USAGE.md)

## Testing

#### (Optional) Set testing environment variables

Change testing app variables by setting values in [test_env](/tests/test_env) file.

#### Run all tests:
```bash
`pytest`
```

#### Run specific test:
```bash
`pytest tests/[<test_file.py>]`
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

### Girma Eshete aka Menelik Berhan
[Linkedin](https://www.linkedin.com/in/menelikberhan)

## License
[MIT](/LICENSE)

[^1]: To avoid: PIL.Image.DecompressionBombError: Image size (... pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack.

[^2]: All language models, except `amh-old`, are from tesseract best language models. `amh-old` is a fine tuned `amh` model using training datas from old amharic printed documents (mostly around the 1950's).

[1]: https://github.com/MenelikBerhan/amharic_ocr_draft
[2]: https://github.com/tesseract-ocr/tessdata_best

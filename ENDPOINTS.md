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

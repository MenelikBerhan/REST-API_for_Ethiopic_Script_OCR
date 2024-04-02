#!/usr/bin/python3
"""Pdf models
"""
from enum import Enum
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.functional_validators import BeforeValidator
from typing import List, Union
from typing_extensions import Annotated
from typing import Dict
import json


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model and as `ObjectId` in database.
PyObjectId = Annotated[str, BeforeValidator(str)]


class OcrOutputFormat(str, Enum):
    """
    ### Output file formats for pdf's OCR result.
    """
    string = 'str'
    """Default mode.(No file saved)"""
    text = 'txt'
    """For plain text file"""
    mswrod = 'docx'
    """For Microsoft Word file."""
    pdf = 'pdf'
    """For pdf file."""


class PdfPostRequestModel(BaseModel):
    """
    ### An Optional Request body of `POST /pdf/` for pdf properties.

    ### A serialized dictionary (`str`:`str`) of pdf properties.\
    (All fields are optional)
    """
    # pdf fields to be set from request body
    description: str = Field(
        default='', description='__Brief description of the pdf.__')

    ocr_output_formats: List[OcrOutputFormat] = Field(
        default=['str'], min_length=1,
        description="""__List of desired OCR output file formats. (_By default
        OCR result is saved in string form_).<br><br>If the result is also to
        be saved in file, and readily available as a response for
        `GET /ocr/pdf/{pdf_id}/`,<br>one or more of `txt`, `docx` or `pdf`
        must be passed when posting pdf.<br><br>After posting the pdf use
        the `GET /ocr/pdf/{pdf_id}/` endpoint to get result in any format.
        <br>String output is included in `GET /pdf/[{pdf_id}]` response by
        default.__
        """
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'description': 'Sample pages from amharic-amharic dictionary',
                'ocr_output_formats': ['str', 'txt']
            }
        },
    )

    # validate data when request is passed as string using Form. Used for
    # endpoints having File parameters (Content-type: multipart/form-data)
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if value is None or value == '':
            return {}
        if isinstance(value, str):
            return cls(**json.loads(value))

        return value


class PdfPostResponseModel(PdfPostRequestModel, APIBaseModel):
    """
    ### Abstraction of a Pdf in Response body for `POST /pdf/`.
    """
    name: str = Field(..., description="__Uploaded pdf's filename.__")

    ocr_finished: bool = Field(
        default=False,
        description='__True if background task performing OCR is finished.__')

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'images.pdf',
                'description': 'Sample pages from amharic-amharic dictionary',
                'ocr_output_formats': ['str', 'txt'],
                'ocr_finished': False
            }
        },
    )


class PdfGetResponseModel(PdfPostResponseModel):
    """
    ### Abstraction of a Pdf in Response body for `GET /pdf/`.
    """
    # informations about pdf
    pdf_version: Union[str, None] = Field(
        default=None,
        description='__Portable Document Format (PDF) version.__',
        examples=['1.7'])

    no_pages: Union[int, None] = Field(
        default=None,
        description='__Number of pages in the pdf.__'
    )

    file_size: Union[str, None] = Field(
        default=None,
        description='__Size of pdf file in bytes.__',
        examples=['676660 bytes'])

    page_size: Union[str, None] = Field(
        default=None,
        description='__Size of pdf pages in points (1 pts = 1/72 inch).__',
        examples=['841.92 x 1190.52 pts (A3)'])

    producer: Union[str, None] = Field(
        default=None,
        description='__Program (software) used to create the pdf.__',
        examples=['Microsoft: Print To PDF'])

    # id of TesseractConfigurationModel (`str` in model & `ObjectId` in db)
    tess_config_id: Union[PyObjectId, None] = Field(
        default=None,
        description='__Id of tesseract configuration used for OCR.__')

    # id of TesseractOutputModel (`str` in model & `ObjectId` in db)
    tess_output_id: Union[PyObjectId, None] = Field(
        default=None,
        description='__Id of tesseract output containing OCR results.__')

    # average confidence of recognized words for each page
    ocr_accuracy: Union[Dict[str, float], None] = Field(
        default=None,
        description='__Average OCR confidence level of all pages in the pdf.__'
    )

    # results of OCR as text for each page
    ocr_result_text: Union[Dict[str, str], None] = Field(
        default=None,
        description='__Result of OCR for each page in string form.__'
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'images.pdf',
                'description': 'Sample pages from amharic-amharic dictionary',
                'ocr_output_formats': ['str', 'txt'],
                'page_size': '841.92 x 1190.52 pts (A3)',
                'no_pages': 2,
                'producer': 'Microsoft: Print To PDF',
                'file_size': '676660 bytes',
                'pdf_version': '1.7',
                'ocr_finished': True,
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
                'tess_output_id': '66008f3a64bd72e19e40a43a',
                'ocr_accuracy': {"1": 90.64, "2": 89.95},
                'ocr_result_text': {
                    '1': 'ከምስል ላይ የተለቀሙ የአማርኛ ፊደላት። ...',
                    '2': 'ኢትዮጵያ ትቅደም! ...'},
            }
        },  # type: ignore
    )


class PdfModel(PdfGetResponseModel):
    """
    ### A model class for abstraction of a Pdf stored in Database.
    """
    # fields not in response model (but stored in db)
    local_path: Union[str, None] = Field(
        default=None, description='__Local storage path of the pdf.__')

    done_output_formats: Dict[OcrOutputFormat, str] = Field(
        default={},
        description="""Key value pair of saved output file formats
        and their path in local storage."""
    )

    # # image related info about each page
    # pages_info: Union[Dict[str, Dict[str, Any]], None] = Field(
    #     default=None,
    #     description="__Image related info about pdf's pages.__"
    # )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'images.pdf',
                'description': 'Sample pages from amharic-amharic dictionary',
                'ocr_output_formats': ['str', 'txt'],
                'page_size': '841.92 x 1190.52 pts (A3)',
                'no_pages': 2,
                'producer': 'Microsoft: Print To PDF',
                'file_size': '676660 bytes',
                'pdf_version': '1.7',
                'ocr_finished': True,
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
                'tess_output_id': '66008f3a64bd72e19e40a43a',
                'ocr_accuracy': {"1": 90.64, "2": 89.95},
                'ocr_result_text': {
                    '1': 'ከምስል ላይ የተለቀሙ የአማርኛ ፊደላት። ...',
                    '2': 'ኢትዮጵያ ትቅደም! ...'},
                'local_path':
                    '/ocr/images_c34bbe0d-298c-4fe0-a799-e57b885d0375.pdf',
                'done_output_formats': {
                    'txt': '/ocr/pdf_c34bbe0d-298c-4fe0-a799-e57b885d0375.txt'
                    }
            }
        },  # type: ignore
    )


class PdfCollection(BaseModel):
    """
    ### A container holding a list of `PdfGetResponseModel` instances.

    ### This exists because providing a top-level array in a JSON response\
    can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx)
    """  # noqa
    # list of pdfs
    pdfs: List[PdfGetResponseModel]

#!/usr/bin/python3
"""Images model
"""
from enum import Enum
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.functional_validators import BeforeValidator
from typing import List, Tuple, Union
from typing_extensions import Annotated
from typing import Dict
import json


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model and as `ObjectId` in database.
PyObjectId = Annotated[str, BeforeValidator(str)]


class OcrOutputFormat(str, Enum):
    """
    ### Output file formats for image's OCR result.
    """
    string = 'str'
    """Default mode.(No file saved)"""
    text = 'txt'
    """For plain text file"""
    mswrod = 'docx'
    """For Microsoft Word file."""
    pdf = 'pdf'
    """For pdf file."""


class ImagePostRequestModel(BaseModel):
    """
    ### An Optional Request body of `POST /images/` for image properties.

    ### A serialized dictionary (`str`:`str`) of image properties.\
    (All fields are optional)
    """
    # image fields to be set from request body
    description: str = Field(
        default='', description='__Brief description of the image.__')

    ocr_output_formats: List[OcrOutputFormat] = Field(
        default=['str'], min_length=1,
        description="""__List of desired OCR output file formats. (_By default
        OCR result is saved in string form_).<br><br>If the result is also to
        be saved in file, and readily available as a response for
        `GET /ocr/{image_id}/`,<br>one or more of `txt`, `docx` or `pdf` must
        be passed when posting image.<br><br>After posting the image use the
        `GET /ocr/{image_id}/` endpoint to get result in any format.<br>String
        output is included in `GET /images/[{image_id}]` response by default.__
        """
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'description': 'Sample page from amharic-amharic dictionary',
                'ocr_output_formats': ['txt']
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


class ImagePostResponseModel(ImagePostRequestModel, APIBaseModel):
    """
    ### Abstraction of an Image in Response body for `POST /images`.
    """
    name: str = Field(..., description="__Uploaded image's filename.__")

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
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
                'ocr_output_formats': ['txt'],
                'ocr_finished': False
            }
        },
    )


# used to hide properties like `local_path` that will be stored in db
class ImageGetResponseModel(ImagePostResponseModel):
    """
    ### Abstraction of an Image in Response body for `GET /images`.
    """
    # id of TesseractConfigurationModel (`str` in model & `ObjectId` in db)
    tess_config_id: Union[PyObjectId, None] = Field(
        default=None,
        description='__Id of tesseract configuration used for OCR.__')

    # id of TesseractOutputModel (`str` in model & `ObjectId` in db)
    tess_output_id: Union[PyObjectId, None] = Field(
        default=None,
        description='__Id of tesseract output containing OCR results.__')

    # fields populated by background process after POST /images
    ocr_result_text: Union[str, None] = Field(
        default=None,
        description="__Result of OCR by tesseract in string form.__")

    image_size: Union[Tuple[int, int], None] = Field(
        default=None,
        description='__`(width, height)` of the image in pixles.__',
        examples=[(909, 526)])

    image_format: Union[str, None] = Field(
        default=None,
        description='__Type of image file.__',
        examples=['PNG', 'JPEG', 'TIFF', 'GIF', 'BMP'])

    image_mode: Union[str, None] = Field(
        default=None,
        description='__Mode of an image that defines the type and\
            depth of a pixel in the image.__',
        examples=[
            'L (8-bit pixels, grayscale)',
            'P (8-bit pixels, mapped to any other mode using a color palette)',
            'RGB (3x8-bit pixels, true color)',
            'RGBA (4x8-bit pixels, true color with transparency mask)',
            'CMYK (4x8-bit pixels, color separation)'])

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
                'image_size': (909, 526),
                'image_format': 'PNG',
                'image_mode': 'RGB',
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
                'tess_output_id': '66008f3a64bd72e19e40a43a',
                'ocr_output_formats': ['txt'],
                'ocr_finished': True,
                'ocr_result_text': 'ከምስል ላይ የተለቀሙ የአማርኛ ፊደላት።',
            }
        },  # type: ignore
    )


class ImageModel(ImageGetResponseModel):
    """
    ### A model class for abstraction of an Image stored in Database.
    """
    # fields not in response model (but stored in db)
    local_path: Union[str, None] = Field(
        default=None, description='__Local storage path of image.__')

    info: Union[dict, None] = Field(
        default=None,
        description='A dictionary holding data associated with the image.',
        examples=[
            {'srgb': 0, 'gamma': 0.45455, 'dpi': (95.9866, 95.9866)},
            {'jfif': 257, 'jfif_version': (1, 1), 'jfif_unit': 0,
             'jfif_density': (1, 1)}])

    done_output_formats: Dict[OcrOutputFormat, str] = Field(
        default={},
        description="""Key value pair of saved output file formats
        and their path in local storage."""
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
                'image_size': (909, 526),
                'image_format': 'PNG',
                'image_mode': 'RGB',
                'info': {'srgb': 0, 'gamma': 0.45455, 'dpi': (96, 96)},
                'local_path':
                    '/ocr/image_c34bbe0d-298c-4fe0-a799-e57b885d0375.png',
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
                'ocr_output_formats': ['txt'],
                'ocr_finished': True,
                'ocr_result_text': 'ከምስል ላይ የተለቀሙ የአማርኛ ፊደላት።',
                'done_output_formats': {
                    'txt': '/ocr/image_c34bbe0d-298c-4fe0-a799-e57b885d0375.'
                    }
            }
        },  # type: ignore
    )


class ImageCollection(BaseModel):
    """
    ### A container holding a list of `ImageGetResponseModel` instances.

    ### This exists because providing a top-level array in a JSON response\
    can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx)
    """  # noqa
    # list of images
    images: List[ImageGetResponseModel]

#!/usr/bin/python3
"""Images model
"""
from enum import Enum
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Union, Dict
import json


# TODO: use Field for fields & add field desctiptions
class Language(str, Enum):
    """### Available OCR languages"""
    amharic = 'amh'
    amharic_old = 'amh-old'
    """Fine tuned amharic model (using old prints)"""
    english = 'eng'
    tigrigna = 'tig'


class OcrOutputFormat(str, Enum):
    """### OCR result output formats.

    ### By default OCR result is saved in string form. If the result is to be\
    saved in file, one of `txt`, `docx` or `pdf` must be passed. After\
    uploading the image one can also use the `GET /ocr/{image_id}/` endpoint\
    to get result in other formats."""

    string = 'str'
    """Default mode."""
    text = 'txt'
    """For plain text file"""
    mswrod = 'docx'
    """For Microsoft Word file."""
    pdf = 'pdf'
    """For pdf file."""


class TesseractConfigRequestModel(BaseModel):
    """
    ### An Optional Request body of `POST /images/` for tesseract configuration.

    ### A serialized dictionary (`str`:`str`) of tesseract config parameters.\
    (All fields are optional)
    
    ### Refer [TESSERACT(1) Manual Page](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options)

    ### Check [tesseract_parameters](https://github.com/MenelikBerhan/REST-API_for_Ethiopic_Script_OCR/blob/image_ocr/utils/default_tesseract_parameters)\
    file for list of configurable tesseract variables to use for `config_vars`.
    """  # noqa
    output_format: OcrOutputFormat = Field(
        default=OcrOutputFormat.string,
        description="""__OCR output file format. By default OCR result is saved
        in string form. If the result is to be saved in file, one of `txt`,
        `docx` or `pdf` must be passed. After uploading the image use the
        `GET /ocr/{image_id}/` endpoint to get result in other formats.__
        """
    )

    language: Language = Field(
        default=Language.amharic_old,
        description='__Language of text in image.__')

    oem: int = Field(
        default=1, ge=0, le=3,
        description='__OCR engine mode used by tesserat.__')

    psm: int = Field(
        default=3, ge=0, le=13,
        description='__Page segmentation mode used by tesseract.__')

    # additional custom configuration flags
    # TODO: validate key names by cross checking with tesseract_parameters file
    config_vars: Dict[str, Union[int, float]] = Field(
        default={},
        description="__`Key: value` pairs of tesseract config variables \
            (`CONFIGVAR`). Passed to tesseract using multiple `-c`.__"
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'output_format': 'str',
                'language': 'amh-old',
                'oem': 1,
                'psm': 3,
                'config_vars': {
                    'load_system_dawg': 0,
                    'preserve_interword_spaces': 1,
                    }
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


class TesseractConfigModel(APIBaseModel, TesseractConfigRequestModel):
    """
    ### A model class for abstraction of tesseract configuration.
    """

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'output_format': 'str',
                'language': 'amh-old',
                'oem': 1,
                'psm': 3,
                'config_vars': {
                    'load_system_dawg': 0,
                    'preserve_interword_spaces': 1,
                    }
            }
        },
    )

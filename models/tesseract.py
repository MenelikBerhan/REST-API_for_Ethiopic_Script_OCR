#!/usr/bin/python3
"""Images model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import List, Tuple, Union
import json
from enum import Enum


class Language(str, Enum):
    """Available OCR languages"""
    amharic = 'amh'
    english = 'eng'
    tigrigna = 'tig'


class TesseractConfigRequestModel(BaseModel):
    """
    An Optional Request body of `POST /images/` for tesseract configuration.

    A serialized dictionary (`str`:`str`) of tesseract config parameters.
    Refer [TESSERACT(1) Manual Page](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options)
    """
    language: Language = Field(
        default=Language.amharic,
        description='Language of text in image.')

    oem: int = Field(
        default=1, ge=0, le=3,
        description='OCR engine mode used by tesserat.')

    psm: int = Field(
        default=3, ge=0, le=13,
        description='Page segmentation mode used by tesseract.')

    # TODO: add other relevant Tesseract CONFIGVARS here

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'language': 'amh',
                'oem': 1,
                'psm': 3,
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
    A model class for abstraction of tesseract configuration.
    """

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'language': 'amh',
                'oem': 1,
                'psm': 3,
            }
        },
    )

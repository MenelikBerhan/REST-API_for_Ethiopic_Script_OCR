#!/usr/bin/python3
"""Images model
"""
from enum import Enum
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Union, Dict
import json


class Language(str, Enum):
    """Available OCR languages"""
    amharic = 'amh'
    amharic_old = 'amh-old'
    """Fine tuned amharic model (using old prints)"""
    english = 'eng'
    tigrigna = 'tig'


class TesseractConfigRequestModel(BaseModel):
    """### An Optional Request body of `POST /images/` for tesseract configuration.

    ### A serialized dictionary (`str`:`str`) of tesseract config parameters.
    
    ### Refer [TESSERACT(1) Manual Page](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options)

    ### Check [tesseract_parameters](https://github.com/MenelikBerhan/REST-API_for_Ethiopic_Script_OCR/blob/image_ocr/utils/default_tesseract_parameters)\
    file for list of configurable tesseract variables to use for `config_vars`.
    """  # noqa
    language: Language = Field(
        default=Language.amharic_old,
        description='Language of text in image.')

    oem: int = Field(
        default=1, ge=0, le=3,
        description='OCR engine mode used by tesserat.')

    psm: int = Field(
        default=3, ge=0, le=13,
        description='Page segmentation mode used by tesseract.')

    # additional custom configuration flags
    # TODO: validate key names by cross checking with tesseract_parameters file
    config_vars: Dict[str, Union[int, float]] = Field(
        default={},
        description="`Key: value` pairs of tesseract config variables \
            (`CONFIGVAR`). Passed to tesseract using `-c`."
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
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
                'config_vars': {
                    'load_system_dawg': 0,
                    'preserve_interword_spaces': 1,
                    }
            }
        },
    )

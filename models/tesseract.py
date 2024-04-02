#!/usr/bin/python3
"""Images model
"""
from bson import ObjectId
from enum import Enum
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.functional_validators import BeforeValidator
from typing import Dict, List, Union
from typing_extensions import Annotated
import json

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model and as `ObjectId` in database.
PyObjectId = Annotated[str, BeforeValidator(str)]


# TODO: use Field for fields & add field desctiptions
class Language(str, Enum):
    """### Available OCR language models."""
    amharic = 'amh'
    amharic_old = 'amh-old'
    """Fine tuned amharic model (using old prints)"""
    english = 'eng'
    tigrigna = 'tig'


class ImagePreprocessing(str, Enum):
    """### Type of image preprocessing used."""
    none = 'none'
    simple = 'simple'
    detailed = 'detailed'


class TesseractConfigRequestModel(BaseModel):
    """
    ### An Optional Request body of `POST /image/` for tesseract configuration.

    ### A serialized dictionary (`str`:`str`) of tesseract config parameters.\
    (All fields are optional)
    
    ### Refer [TESSERACT(1) Manual Page](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#options)

    ### Check [tesseract_parameters](https://github.com/MenelikBerhan/REST-API_for_Ethiopic_Script_OCR/blob/image_ocr/utils/default_tesseract_parameters)\
    file for list of configurable tesseract variables to use for `config_vars`.
    """  # noqa

    language: Language = Field(
        default=Language.amharic_old,
        description='__Tesseract language model to use for OCR.__')

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
        if cls.__name__ == 'TesseractConfigRequestModel':
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


class TesseractOutputModelImage(APIBaseModel):
    """
    Model class for abstraction of image's tesseract OCR result.
    """
    image_id: ObjectId = Field(
        ...,
        description="Images id."
    )

    tess_config_id: ObjectId = Field(
        ...,
        description='Tesseract configuration id.'
    )

    image_preprocessing: ImagePreprocessing = Field(
        default=ImagePreprocessing.none,
        description='Type of image preprocessing used.'
    )

    time_taken: float = Field(
        ...,
        description='Time taken to OCR the image.'
    )

    ocr_accuracy: float = Field(
        ...,
        description='Average confidence level of words recognized.'
    )

    ocr_result_text: str = Field(
        ...,
        description="OCR result in string form."
        )

    ocr_result_dict: Dict[str, Union[List[int], List[str]]] = Field(
        ...,
        description="""A dictionary containing detailed OCR result.
        Contains information about recognized words location in the input
        image and the confidence they are recognized with.
        [`level`, `page_num`, `block_num`, `par_num`, `line_num`, `word_num`,
        `left`, `top`,  `width`, `height`, `conf` and `text`]."""
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'image_id': '65fb7cc253b139befea1205c',
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
                'image_preprocessing': 'simple',
                'time_taken': 3.95,
                'ocr_accuracy': 87.8,
                'ocr_result_text': 'ከምስል ላይ የተለቀሙ የአማርኛ ፊደላት።',
                'ocr_result_dict': {
                    'level': [1, 2], 'page_num': [1, 1], 'block_num': [0, 1],
                    'par_num': [0, 0], 'line_num': [0, 1], 'word_num': [0, 1],
                    'left': [0, 254], 'top': [0, 29], 'width': [644, 65],
                    'height':  [56, 17], 'conf': [-1, 92], 'text': ['', 'ምንሊክ']
                }
            }
        },  # type: ignore
    )


class TesseractOutputModelPdf(APIBaseModel):
    """
    Model class for abstraction of pdf's tesseract OCR result.
    """
    pdf_id: ObjectId = Field(
        ...,
        description="Pdf's id."
    )

    tess_config_id: ObjectId = Field(
        ...,
        description='Tesseract configuration id.'
    )

    image_preprocessing: ImagePreprocessing = Field(
        default=ImagePreprocessing.none,
        description='Type of image preprocessing used.'
    )

    time_taken: Dict[str, float] = Field(
        ...,
        description='Time taken to OCR each pdf pages.'
    )

    ocr_accuracy: Dict[str, float] = Field(
        ...,
        description="""Average confidence level of words recognized for each
        page."""
    )

    ocr_result_text: Dict[str, str] = Field(
        ...,
        description="OCR result in string form for each page."
        )

    ocr_result_dict: Dict[str, Dict[str, Union[List[int], List[str]]]] = Field(
        ...,
        description="""Dictionary containing detailed OCR result for each page.
        Contains information about recognized words location in the input
        image and the confidence they are recognized with.
        [`level`, `page_num`, `block_num`, `par_num`, `line_num`, `word_num`,
        `left`, `top`,  `width`, `height`, `conf` and `text`]."""
    )

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'image_id': '65fb7cc253b139befea1205c',
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
                'image_preprocessing': 'simple',
                'time_taken': {'1': 12.11, '2': 9.92},
                'ocr_accuracy': {"1": 90.64, "2": 89.95},
                'ocr_result_text': {
                    '1': 'ከምስል ላይ የተለቀሙ የአማርኛ ፊደላት። ...',
                    '2': 'ኢትዮጵያ ትቅደም! ...'},
                'ocr_result_dict': {
                    '1': {'level': [1, 2], 'page_num': [1, 1], 'block_num': [0, 1],
                    'par_num': [0, 0], 'line_num': [0, 1], 'word_num': [0, 1],
                    'left': [0, 254], 'top': [0, 29], 'width': [644, 65],
                    'height':  [56, 17], 'conf': [-1, 92], 'text': ['', 'ምንሊክ']}
                }
            }
        },  # type: ignore
    )

#!/usr/bin/python3
"""Images model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import List, Union
import json


class ImageModel(APIBaseModel):
    """
    A model class for abstraction of an Image.
    """
    # set image fields
    name: str = Field(...)
    dpi: int = Field(default=300, description='Dots per Inch')

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'image.png',
                'dpi': 300
            }
        },
    )

    # validate data when request is passed as string using Form. Used for
    # endpoints having File parameters (Content-type: multipart/form-data)
    # @model_validator(mode='before')
    # @classmethod
    # def validate_to_json(cls, value):
    #     if isinstance(value, str):
    #         return cls(**json.loads(value))
    #     return value


class ImageCollection(BaseModel):
    """
    A container holding a list of `Image` instances.

    This exists because providing a top-level array in a JSON response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    # list of images
    images: List[ImageModel]


class ImageRequestBody(BaseModel):
    """
    Model for Request body of `POST /images/`.

    All fields are Optional.
    """
    # set image fields
    name: Union[str, None] = Field(default=None)

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'image.png',
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

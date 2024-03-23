#!/usr/bin/python3
"""Images model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import List, Union
import json

# used to hide properties like `local_path`
class ImageResponseModel(APIBaseModel):
    """
    A model class for abstraction of an Image in Response bodies.
    """
    name: str = Field(..., description="Uploaded image's filename.")
    description: Union[str, None] = Field(default=None, description='Brief description of the image.')
    dpi: int = Field(default=300, description='Dots per Inch')


    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
                'dpi': 300,
            }
        },
    )


class ImageModel(ImageResponseModel):
    """
    A model class for abstraction of an Image stored in Database.
    """
    # fields not in response model (but stored in db)
    local_path: str = Field(...)

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
                'dpi': 300,
                'local_path': '/tmp/ocr_app/image_c34bbe0d-298c-4fe0-a799-e57b885d0375.png',
            }
        },
    )


class ImageCollection(BaseModel):
    """
    A container holding a list of `Image` instances.

    This exists because providing a top-level array in a JSON response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    # list of images
    images: List[ImageResponseModel]


class ImageRequestBody(BaseModel):
    """
    An Optional Request body of `POST /images/`.

    A dictionary (`str`:`str`) of image properties. (All fields are optional)
    """
    # image fields to be set from request body
    description: Union[str, None] = Field(default=None, description='Brief description of the image.')

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
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

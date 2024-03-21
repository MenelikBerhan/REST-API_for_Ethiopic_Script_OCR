#!/usr/bin/python3
"""Images model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field
from typing import List


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


class ImageCollection(BaseModel):
    """
    A container holding a list of `Image` instances.

    This exists because providing a top-level array in a JSON response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    # list of images
    images: List[ImageModel]

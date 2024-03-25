#!/usr/bin/python3
"""Images model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.functional_validators import BeforeValidator
from typing import List, Tuple, Union
from typing_extensions import Annotated
from typing import Optional
import json


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model and as `ObjectId` in database.
PyObjectId = Annotated[str, BeforeValidator(str)]


class ImagePostResponseModel(APIBaseModel):
    """
    Abstraction of an Image in Response body for `POST /images`.
    """
    name: str = Field(..., description="Uploaded image's filename.")
    description: Union[str, None] = Field(default=None, description='Brief description of the image.')

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': '65fb7cc253b139befea1205c',
                'created_at': '2024-03-21T00:18:10.836000',
                'updated_at': '2024-03-21T00:18:10.836000',
                'name': 'image.png',
                'description': 'Sample page from amharic-amharic dictionary',
            }
        },
    )


# used to hide properties like `local_path` that will be stored in db
class ImageGetResponseModel(ImagePostResponseModel):
    """
    Abstraction of an Image in Response body for `GET /images`.
    """
    # id of TesseractConfigurationModel (`str` in model & `ObjectId` in db)
    tess_config_id: Optional[PyObjectId] = Field(default=None)

    # fields populated by background process after POST /images
    image_size: Union[Tuple[int, int], None] = Field(default=None,
                                        description='(width, height) of the image in pixles.',
                                        examples=[(909, 526)]
                                        )
    image_format: Union[str, None] = Field(default=None,
                              description='Type of image file.',
                              examples=['PNG', 'JPEG', 'TIFF', 'GIF', 'BMP'])
    image_mode: Union[str, None] = Field(default=None,
                            description='Mode of an image that defines the type and depth of a pixel in the image.',
                            examples=[
                                'L (8-bit pixels, grayscale)', 
                                'P (8-bit pixels, mapped to any other mode using a color palette)',
                                'RGB (3x8-bit pixels, true color)',
                                'RGBA (4x8-bit pixels, true color with transparency mask)',
                                'CMYK (4x8-bit pixels, color separation)'
                            ])
    info: Union[dict, None] = Field(default=None,
                       description='A dictionary holding data associated with the image.',
                       examples=[
                           {'srgb': 0, 'gamma': 0.45455, 'dpi': (95.9866, 95.9866)},
                           {'jfif': 257, 'jfif_version': (1, 1), 'jfif_unit': 0, 'jfif_density': (1, 1)},
                       ])

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
                'info': {'srgb': 0, 'gamma': 0.45455, 'dpi': (95.9866, 95.9866)},
                'tess_config_id': '66008f3a64bd72e19e40aa7e',
            }
        }, # type: ignore
    )


class ImageModel(ImageGetResponseModel):
    """
    A model class for abstraction of an Image stored in Database.
    """
    # fields not in response model (but stored in db)
    local_path: Union[str, None] = Field(default=None, description='Local storage path of image.')

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
                'info': {'srgb': 0, 'gamma': 0.45455, 'dpi': (95.9866, 95.9866)},
                'local_path': '/tmp/ocr_app/image_c34bbe0d-298c-4fe0-a799-e57b885d0375.png',
            }
        }, # type: ignore
    )


class ImageCollection(BaseModel):
    """
    A container holding a list of `ImageGetResponseModel` instances.

    This exists because providing a top-level array in a JSON response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    # list of images
    images: List[ImageGetResponseModel]


class ImageRequestBody(BaseModel):
    """
    An Optional Request body of `POST /images/`.

    A serialized dictionary (`str`:`str`) of image properties. (All fields are optional)
    """
    # image fields to be set from request body
    description: Union[str, None] = Field(default=None, description='Brief description of the image.')

    # add config
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
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

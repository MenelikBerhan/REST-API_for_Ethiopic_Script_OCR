#!/usr/bin/python3
"""Base model
"""
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from typing import Optional


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model and as `ObjectId` in database.
PyObjectId = Annotated[str, BeforeValidator(str)]


class APIBaseModel(BaseModel):
    """Base model class for abstraction of objects in the OCR app API.
    (Images, PDFs, Tesseract configuration, output & training, and Users.)

    Attributes:
        created_at (DateTime)   : object creation time stamp
        updated_at (DateTime)   : time stamp for last update on object
        id (str)                : unique identifying string

    """
    # The primary key for the object in db (`str` in model & `ObjectId` in db)
    # Needs to be aliased since `_id` will be considered by pydentic as private
    id: Optional[PyObjectId] = Field(alias='_id', default=None)

    # created & updated time stamp with timezone
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # configure Pydantic behaviour. (by name not to use aliase)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


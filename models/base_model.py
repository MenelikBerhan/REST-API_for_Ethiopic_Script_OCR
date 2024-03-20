#!/usr/bin/python3
"""Base model
"""


class BaseModel:
    """Base model class for abstraction of objects in the OCR app.
    (Images, PDFs, Tesseract configuration, output & training, and Users.)

    Attributes:
        created_at (DateTime)   : object creation time stamp
        updated_at (DateTime)   : time stamp for last update on object
        id (str)                : unique identifying string

    """

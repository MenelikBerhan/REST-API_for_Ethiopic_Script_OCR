"""Utilities CRUD operations on DB
"""
from bson import ObjectId
from bson.errors import InvalidId
from db.mongodb import db_client
from fastapi import HTTPException, status


async def get_image_by_id(image_id: str) -> dict:
    """Find & return image from db based on id."""
    # retrieve image from db
    try:
        image = await db_client.db.images.find_one({'_id': ObjectId(image_id)})
    except InvalidId:   # handle invalid ObjectId string
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"""InvalidId: '{image_id}' is not a valid ObjectId, it must be \
a 12-byte input or a 24-character hex string""")

    if image is None:   # image not found in db
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Image with given id: '{image_id}' doesn't exist.")

    return image


async def get_pdf_by_id(pdf_id: str) -> dict:
    """Find & return pdf from db based on id."""
    # retrieve pdf from db
    try:
        pdf = await db_client.db.pdfs.find_one({'_id': ObjectId(pdf_id)})
    except InvalidId:   # handle invalid ObjectId string
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"""InvalidId: '{pdf_id}' is not a valid ObjectId, it must be \
a 12-byte input or a 24-character hex string""")

    if pdf is None:   # pdf not found in db
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Pdf with given id: '{pdf_id}' doesn't exist.")

    return pdf

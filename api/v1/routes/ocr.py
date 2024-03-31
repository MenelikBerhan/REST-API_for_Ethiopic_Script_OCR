"""Ocr endpoints
"""
from bson import ObjectId
from bson.errors import InvalidId
from db.mongodb import db_client
from fastapi import APIRouter, HTTPException, status
from models.images import OcrOutputFormat
from typing import List


# create a router with `/images` prefix
ocr_router = APIRouter(prefix='/ocr')


@ocr_router.get(
    '/done/{image_id}',
    response_description='__List of Finished OCR output formats__',
)
async def ready_outputs(image_id: str) -> List[OcrOutputFormat]:
    """
    ### List of file formats the OCR result is already saved in.<br>\
    Output file is readily available for file formats in this list.

    ### To add formats not in response list use GET `/ocr/{image_id}/`\
    endpoint.
    """
    try:
        image = await db_client.db.images.find_one({'_id': ObjectId(image_id)})
    except InvalidId:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"""InvalidId: '{image_id}' is not a valid ObjectId, it must be \
a 12-byte input or a 24-character hex string""")

    if image is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Image with given id: '{image_id}' doesn't exist.")

    return list(image['done_output_formats'].keys())

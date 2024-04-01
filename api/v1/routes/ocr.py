"""Ocr endpoints
"""
from bson import ObjectId
from bson.errors import InvalidId
from db.mongodb import db_client
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse, JSONResponse
from models.images import OcrOutputFormat
from typing import List


# create a router with `/images` prefix
ocr_router = APIRouter(prefix='/ocr')


async def get_image_by_id(image_id: str) -> dict:
    """Find & return image from db based on id."""
    # retrieve image from db
    try:
        image = await db_client.db.images.find_one({'_id': ObjectId(image_id)})
    except InvalidId:   # handle invalid ObjectId string
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"""InvalidId: '{image_id}' is not a valid ObjectId, it must be \
a 12-byte input or a 24-character hex string""")

    if image is None:   # image not found in db
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Image with given id: '{image_id}' doesn't exist.")

    return image


@ocr_router.get(
    '/image/done/{image_id}',
    response_description='__List of Saved OCR output formats__',
)
async def get_ocr_output_file_formats(image_id: str) -> List[OcrOutputFormat]:
    """
    ### List of file formats the OCR result is already saved in.<br>\
    Output file is readily available for file formats in this list.

    ### To add formats not in response list use GET `/image/ocr/{image_id}/`\
    endpoint.
    """
    # retrieve image from db
    image = await get_image_by_id(image_id)

    # return list of formats OCR result is already saved in
    return list(image['done_output_formats'].keys())


@ocr_router.get(
    '/image/{image_id}',
    response_description="__Image's OCR result__",
    response_class=FileResponse
)
async def get_ocr_result(
    image_id: str,
    format: OcrOutputFormat = Query(
        default='str',
        description="__File format of image's OCR result__"
        ),
    add_format: bool = Query(
        default=False,
        description="""__If OCR output is not already saved in given format,
        Save OCR output in given format and add it to list of
        `ocr_output_formats` field of the image.__
        """
        )):
    """
    ### Get images OCR result as a string or a file.
    """
    print(image_id)
    # retrieve image from db
    image = await get_image_by_id(image_id)

    if format == 'str':
        return JSONResponse(image['ocr_result_text'])
    if format not in image['done_output_formats']:
        if add_format:      # create output file in missing format
            return JSONResponse(f"Creating output file for '{format}' format.")

        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"OCR output not ready in '{format}' format.")

    return image['done_output_formats'][format]

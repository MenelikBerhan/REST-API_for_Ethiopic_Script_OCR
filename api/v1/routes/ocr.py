"""Ocr endpoints
"""
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone
from db.mongodb import db_client
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse, JSONResponse
from models.images import OcrOutputFormat
from os import path
from typing import List
from utils.file_read_write import background_write_ocr_result_image


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
    Output file is readily available for file formats in the response list.\
    <br>If the response list is empty, it means *OCR process is not finished*.

    ### To add formats not in response list use GET `/ocr/image/{image_id}/`\
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
    # retrieve image from db
    image = await get_image_by_id(image_id)

    if format == 'str':
        return JSONResponse(image['ocr_result_text'])

    if format not in image['done_output_formats']:
        if not add_format:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Given format '{format}' not in image's `ocr_output_formats` \
list. To add it to the list and get the result set `add_format` \
to `True`.")

        # create output file for missing format
        # add format to list of output formats (not saved in db)
        image['ocr_output_formats'].append(format)

        # write ocr output files & get their path (in returned dict)
        write_ocr_result_dict = await background_write_ocr_result_image(
            image['local_path'], image,
            {'ocr_result_text': image['ocr_result_text']}
        )
        print(
            f"Result Saved in {list(write_ocr_result_dict.keys())} format."
            )

        # update `done_output_formats` dict in image (not saved in db)
        image['done_output_formats'].update(write_ocr_result_dict)

        # create dict for updating image in db
        image_update_dict = {}

        # set images `ocr_output_formats` list and `done_output_formats`
        # in image_update_dict to save the added formats.
        image_update_dict['ocr_output_formats'] = image[
            'ocr_output_formats']

        image_update_dict['done_output_formats'] = image[
            'done_output_formats']

        # set update_at field
        image_update_dict['updated_at'] = datetime.now(timezone.utc)
        # update image in db
        await db_client.db.images.update_one(
            {'_id': image['_id']},
            {'$set': image_update_dict},
            )

    # set output file name from image name
    base_name, _ = path.splitext(image['name'])
    output_file_name = base_name + '_ocr-result.' + format

    return FileResponse(
        image['done_output_formats'][format], filename=output_file_name
        )

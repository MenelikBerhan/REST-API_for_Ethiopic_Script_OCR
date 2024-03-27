"""Image OCR using pytesseract
"""
from bson import ObjectId
from config.setup import settings
from datetime import datetime, timezone
from db.mongodb import db_client
from utils.file_read_write import background_write_file
from utils.tesseract import background_setup_tess_config,\
    background_run_tesseract
import asyncio
import concurrent.futures
import pytesseract as pts


OCR_IN_PROGRESS: int = 0
"""Keeps track of no. of images being processed"""


async def background_image_ocr(
        file_buffer: bytes, file_name: str, id: str, tess_req_dict: dict):
    """Performs OCR on image using background tasks.

    Args:
        file_buffer (bytes): uploaded image as bytes
        file_name (str): name of uploaded image
        id (str): id of image in database
        tess_req_dict (dict): tesseract configuration parameters passed
            in request body
    """
    # set as global (otherwise UnboundLocalError: referenced before assignment)
    global OCR_IN_PROGRESS

    # get tesseract configuration based on given params in request
    config_dict = await background_setup_tess_config(tess_req_dict)
    print('Tesseract: CONFIGURED')

    # save image in local storage & get image_dict (metadata & storage path)
    image, image_dict = await background_write_file(file_buffer, file_name)
    print('Image: WRITTEN 2 LOCAL')

    ocr_result = await background_run_tesseract(image, config_dict)
    print('Tesseract: OCR FINISHED')

    # update image in db
    image_dict.update({
        'ocr_finished': True,
        'ocr_result': ocr_result,
        "tess_config_id": config_dict['id'],
        "updated_at": datetime.now(timezone.utc)})

    await db_client.db.images.update_one(
        {'_id': ObjectId(id)}, {'$set': image_dict})

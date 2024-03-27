"""Image OCR using pytesseract
"""
from bson import ObjectId
from config.setup import settings
from datetime import datetime, timezone
from db.mongodb import db_client
from utils.file_read_write import background_write_file
from utils.tesseract_config import background_setup_tess_config
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
    image, image_dict = await background_write_file(
        file_buffer, file_name, id)
    print('Image: WRITTEN 2 LOCAL')

    # [REFERENCE](https://docs.python.org/3.8/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)  # noqa
    # get the running event loop in the current OS thread
    loop = asyncio.get_running_loop()

    # run tesseract OCR in a custom thread pool. Increase workers if available.
    # (Better efficieny than ProcessPoolExecutor)
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=settings.OCR_WORKERS) as pool:
        # before running OCR on a new image, wait for previous one to finish.
        # if added immediately, executor won't return until all images are done
        while OCR_IN_PROGRESS > 0:
            await asyncio.sleep(2)  # TODO: check d/t sleep durations effect

        OCR_IN_PROGRESS = OCR_IN_PROGRESS + 1

        # await and get ocr result
        ocr_result = await loop.run_in_executor(
            pool, lambda: pts.image_to_string(image, lang='amh-old'))

        image.close()   # as precaution (side effect not clear if not closed)

        OCR_IN_PROGRESS = OCR_IN_PROGRESS - 1
        print('Tesseract: OCR FINISHED')

    # update image in db
    image_dict.update({
        'ocr_finished': True,
        'ocr_result': ocr_result,
        "tess_config_id": config_dict['id'],
        "updated_at": datetime.now(timezone.utc)})

    await db_client.db.images.update_one(
        {'_id': ObjectId(id)}, {'$set': image_dict})

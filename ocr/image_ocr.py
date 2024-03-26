"""Image OCR using pytesseract
"""
from bson import ObjectId
from datetime import datetime, timezone
from db.mongodb import db_client
from utils.file_read_write import background_write_file
from utils.tesseract_config import background_setup_tess_config
import asyncio
import concurrent.futures
import pytesseract as pts


def ocr_image(image):
    """
    Synchronous OCR by tesseract, used in custom process pool.
    Needs to be global to use process pool.
    """
    return pts.image_to_string(image, lang='amh-old')


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
    tasks_before = asyncio.all_tasks()
    while len(tasks_before) > 3:
        await asyncio.sleep(5)
        tasks_before = asyncio.all_tasks()

    # print(f'BEFORE: {len(tasks_before)} tasks: {[(t.get_name()) for t in tasks_before]}') # noqa

    # # 1. Run tesseract OCR in the default loop's executor
    # ocr_result = await loop.run_in_executor(
    #     None, lambda: pts.image_to_string(image, lang='amh-old'))

    # # 2. Run tesseract OCR in a custom thread pool:
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     ocr_result = await loop.run_in_executor(
    #         pool, lambda: pts.image_to_string(image, lang='amh-old'))
    #     print(ocr_result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        ocr_result = await loop.run_in_executor(
            pool, ocr_image, image)
        print('Tesseract: OCR FINISHED')

    # tasks_after = asyncio.all_tasks()
    # print(f'AFTER: {len(tasks_after)} tasks: {[(t.get_name()) for t in tasks_after]}') # noqa

    # update image in db
    image_dict.update({
        'ocr_finished': True,
        'ocr_result': ocr_result,
        "tess_config_id": config_dict['id'],
        "updated_at": datetime.now(timezone.utc)})

    await db_client.db.images.update_one(
        {'_id': ObjectId(id)}, {'$set': image_dict})

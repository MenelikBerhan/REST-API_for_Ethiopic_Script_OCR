"""Image OCR using pytesseract
"""
from bson import ObjectId
from datetime import datetime, timezone
from db.mongodb import db_client
from utils.file_read_write import background_write_file
from utils.tesseract import background_setup_tess_config,\
    background_run_tesseract


async def background_image_ocr(
        file_buffer: bytes, file_name: str, image_id: str, tess_req_dict: dict
        ):
    """Performs OCR on image using background tasks.

    Args:
        file_buffer (bytes): uploaded image as bytes
        file_name (str): name of uploaded image
        image_id (str): id of image in database
        tess_req_dict (dict): tesseract configuration parameters passed
            in request body
    """
    # get tesseract configuration based on given params in request
    tess_config_dict = await background_setup_tess_config(tess_req_dict)
    print('Tesseract: CONFIGURED')

    # save image in local storage & get image_dict (metadata & storage path)
    image, image_dict = await background_write_file(file_buffer, file_name)
    print('Image: WRITTEN 2 LOCAL')

    # run tesseract in background & get output model dict & result text
    tess_output_dict, ocr_result_text = await background_run_tesseract(
        image, image_id, tess_config_dict)
    print('Tesseract: OCR FINISHED')

    # update image in db
    image_dict.update({
        'ocr_finished': True,
        'ocr_result_text': ocr_result_text,
        'tess_output_id': tess_output_dict['id'],
        "tess_config_id": tess_config_dict['id'],
        "updated_at": datetime.now(timezone.utc)})

    await db_client.db.images.update_one(
        {'_id': ObjectId(image_id)},
        {'$set': image_dict, '$push': {'done_output_formats': 'str'}})

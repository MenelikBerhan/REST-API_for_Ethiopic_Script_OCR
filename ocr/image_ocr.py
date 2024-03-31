"""Image OCR using pytesseract
"""
from bson import ObjectId
from datetime import datetime, timezone
from db.mongodb import db_client
from utils.file_read_write import background_write_file,\
    background_write_ocr_result
from utils.tesseract import background_setup_tess_config,\
    background_run_tesseract


async def background_image_ocr(
        file_buffer: bytes, image_dict: dict, tess_req_dict: dict
        ):
    """Performs OCR on image using background tasks.

    Args:
        file_buffer (bytes): uploaded image as bytes
        image_dict (dict): dictionary dump of image in database
        tess_req_dict (dict): tesseract configuration parameters passed
            in request body
    """
    # get tesseract configuration based on given params in request
    tess_config_dict = await background_setup_tess_config(tess_req_dict)
    print('Tesseract: CONFIGURED')

    # save image in local storage & get image_dict (metadata & storage path)
    image, image_update_dict = await background_write_file(
        file_buffer, image_dict['name']
        )
    print('Image: WRITTEN 2 LOCAL')

    # run tesseract in background & get output model dict & result text
    tess_output_dict, ocr_result_text = await background_run_tesseract(
        image, image_dict['id'], tess_config_dict
        )
    print('Tesseract: OCR FINISHED')

    # write OCR result to file (text, word or pdf)
    if image_dict['ocr_output_formats']:
        write_result_dict = await background_write_ocr_result(
            image_update_dict['local_path'], image_dict, tess_output_dict
        )
        print(f"Result Saved in {list(write_result_dict.keys())} formats")

        # add saved outptut formats to `done_output_formats`
        image_update_dict['done_output_formats'] = write_result_dict

    # update image in db
    image_update_dict.update({
        'ocr_finished': True,
        'ocr_result_text': ocr_result_text,
        'tess_output_id': tess_output_dict['id'],
        "tess_config_id": tess_config_dict['id'],
        'updated_at': datetime.now(timezone.utc)
        })

    await db_client.db.images.update_one(
        {'_id': ObjectId(image_dict['id'])},
        {'$set': image_update_dict})

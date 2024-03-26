"""Image OCR using pytesseract
"""
from bson import ObjectId
from db.mongodb import db_client
from models.images import ImageModel
from utils.file_read_write import background_write_file
from utils.tesseract_config import background_setup_tess_config
import pytesseract as pts
import asyncio
import cv2



async def background_image_ocr(file_buffer: bytes, file_name: str, id: str, tess_req_dict: dict):
    """Performs OCR on image using background tasks.

    Args:
        file_buffer (bytes): uploaded image as bytes
        file_name (str): name of uploaded image
        id (str): id of image in database
        tess_req_dict (dict): tesseract configuration parameters passed in request body
    """
    await asyncio.sleep(20) 
    # get tesseract configuration based on given params
    config_dict = await background_setup_tess_config(tess_req_dict)
    # print('CONFIGURED')
    print('Tesseract: CONFIGURED')
    # save image in local storage & update image in db with metadata & storage path
    await background_write_file(file_buffer, file_name, id, config_dict['id'])
    print('Image: WRITTEN 2 LOCAL')

    image_db: ImageModel = await db_client.db.images.find_one({'_id': ObjectId(id)})

    image = cv2.imread(image_db['local_path'])
    
    print('Image: LOADED by CV2')

    loop = asyncio.get_running_loop()
    ocr_result = await loop.run_in_executor(None, lambda: pts.image_to_string(image, lang='amh-old'))

    print('Tesseract: OCR FINISHED')

    # ocr_result = pts.image_to_string(image, lang='amh-old')
    # print(ocr_result)
    # image_db['ocr_finished'] = True
    # image_db['ocr_result'] = ocr_result

    await db_client.db.images.update_one(
        {'_id': ObjectId(id)}, {'$set': {'ocr_result': ocr_result}})

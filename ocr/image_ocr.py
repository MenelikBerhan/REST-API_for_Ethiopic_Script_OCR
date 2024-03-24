"""Image OCR using pytesseract
"""
from utils.file_read_write import background_write_file
from utils.tesseract_config import background_setup_tess_config


async def background_image_ocr(file_buffer: bytes, file_name: str, id: str, tess_req_dict: dict):
    """Performs OCR on image using background tasks.

    Args:
        file_buffer (bytes): uploaded image as bytes
        file_name (str): name of uploaded image
        id (str): id of image in database
        tess_req_dict (dict): tesseract configuration parameters passed in request body
    """
    # get tesseract configuration based on given params
    config_dict = await background_setup_tess_config(tess_req_dict)

    # save image in local storage & update image in db with metadata & storage path
    await background_write_file(file_buffer, file_name, id, config_dict['id'])

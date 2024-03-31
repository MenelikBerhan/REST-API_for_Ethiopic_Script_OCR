"""Utilities for file reading & writing operations
"""
from config.setup import settings
from copy import deepcopy
from os import path, mkdir
from PIL import Image
from uuid import uuid4
import aiofiles
import io


async def background_write_file(file_buffer: bytes, file_name: str):
    """
    Retrieves image metadata from buffer and saves image to local storage.
    Updates image of id `id` with properties retrieved from metadata & local
    storage path.
    """
    storage_path = settings.STORAGE_PATH
    # check if storage path exists & is a directory. If not create one.
    if not (path.isdir(storage_path) or path.exists(storage_path)):
        print(f"Directory doesn't exist at given path: '{storage_path}'")
        mkdir(storage_path)
        print(f"Created storage directory: '{storage_path}")

    # set local file name by appending uuid value before the extension.
    base_name, ext = path.splitext(file_name)
    local_file_name = f'{base_name}_{uuid4()}{ext}'

    # set absolute local storage path by appending file name to storage path
    file_path = path.join(path.abspath(storage_path), local_file_name)

    # load image from bytes buffer using Pillow & BytesIO
    image = Image.open(io.BytesIO(file_buffer))

    # remove unnecessary info that causes errors for large png files
    info = deepcopy(image.info)
    info.pop('icc_profile', None)

    # get image metadata and update image in db with it
    image_dict = {
        "local_path": file_path,
        "image_size": image.size,
        "image_format": image.format,
        "image_mode": image.mode,
        "info": info,
        }

    # save image to local storage asynchronously and return image & dict
    async with aiofiles.open(file_path, 'wb') as new_image_file:
        await new_image_file.write(file_buffer)

    return image, image_dict


async def background_write_ocr_result(
        image_path: str, image_dict: dict, tess_output_dict: dict
        ):
    """
    Writes OCR result to files.

    Args:
        image_path (str): absolute path to image in local storage.
        image_dict (dict): dictionary dump of image in database
        tess_output_dict (dict): dictionary dump of OCR result in db
    """
    write_result_dict = {}
    # write OCR result to a plain text file
    if 'txt' in image_dict['ocr_output_formats']:
        # use image file name in local storage for text file name.
        # Saves in same directory as image
        base_name, _ = path.splitext(image_path)
        txt_file_path = base_name + '.txt'

        async with aiofiles.open(txt_file_path, 'w') as txt_file:
            await txt_file.write(tess_output_dict['ocr_result_text'])
        write_result_dict['txt'] = txt_file_path

    # TODO: add docx & pdf writers (preferably async)
    return write_result_dict

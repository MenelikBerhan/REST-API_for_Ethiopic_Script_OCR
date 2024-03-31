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

"""Utilities for file reading & writing operations
"""
from bson import ObjectId
from config.setup import settings
from datetime import datetime, timezone
from db.mongodb import db_client
from os import path, mkdir
from PIL import Image
from uuid import uuid4
import io


async def background_write_file(file_buffer: bytes, file_name: str, image_id: str, config_id: str):
    """Retrieves image metadata from buffer and saves image to local storage.
    Updates image of id `id` with properties retrieved from metadata & local storage path.
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
    info = image.info
    info.pop('icc_profile', None)

    # get image metadata and update image in db with it
    image_dict = {
        "tess_config_id": config_id,
        "local_path": file_path,
        "image_size": image.size,
        "image_format": image.format,
        "image_mode": image.mode,
        "info": info,
        "updated_at": datetime.now(timezone.utc),
        }

    await db_client.db['images'].update_one({'_id': ObjectId(image_id)}, {'$set': image_dict})

    # save image to local storage. then close file pointer to image 
    image.save(file_path)
    image.close()

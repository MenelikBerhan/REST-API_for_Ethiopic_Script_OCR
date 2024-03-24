"""Utilities for file reading & writing operations
"""
from bson import ObjectId
from config.setup import settings
from db.mongodb import db_client
from fastapi import UploadFile
from os import path, mkdir
from PIL import Image
from uuid import uuid4
import io


async def write_file(file: UploadFile) -> str:
    """Writes file in local storage and return absolute path to file.
    """
    storage_path = settings.STORAGE_PATH
    # check if storage path exists & is a directory. If not create one.
    if not (path.isdir(storage_path) or path.exists(storage_path)):
        print(f"Directory doesn't exist at given path: '{storage_path}'")
        mkdir(storage_path)
        print(f"Created storage directory: '{storage_path}")

    # set file name by appending uuid value before the extension
    # space in image files replaced by `_`
    name, ext = path.splitext(file.filename.replace(' ', '_'))
    file_name = f'{name}_{uuid4()}{ext}'

    # set absolute local storage path by appending file name to storage path
    file_path = path.join(path.abspath(storage_path), file_name)

    # read file bytes
    file_buffer = await file.read()

    # load image from bytes buffer using Pillow & BytesIO
    image = Image.open(io.BytesIO(file_buffer))

    info = image.info

    # remove unnecessary info that causes errors for large png files
    info.pop('icc_profile', None)

    # get & set image info in return dict
    image_dict = {
        "name": file.filename,
        "local_path": file_path,
        "image_size": image.size,
        "image_format": image.format,
        "image_mode": image.mode,
        "info": info,
        }

    # save image to local storage. then close file pointers to image & uploaded file
    image.save(file_path)
    image.close()
    # await file.close()

    return image_dict


async def background_write_file(file_buffer: bytes, file_name: str, id: str):
    """Retrieves image metadata from buffer and saves image to local storage.
    """
    storage_path = settings.STORAGE_PATH
    # check if storage path exists & is a directory. If not create one.
    if not (path.isdir(storage_path) or path.exists(storage_path)):
        print(f"Directory doesn't exist at given path: '{storage_path}'")
        mkdir(storage_path)
        print(f"Created storage directory: '{storage_path}")

    # set absolute local storage path by appending file name to storage path
    file_path = path.join(path.abspath(storage_path), file_name)

    # load image from bytes buffer using Pillow & BytesIO
    image = Image.open(io.BytesIO(file_buffer))

    # remove unnecessary info that causes errors for large png files
    info = image.info
    info.pop('icc_profile', None)

    # get image metadata and update image in db with it
    image_dict = {
        "local_path": file_path,
        "image_size": image.size,
        "image_format": image.format,
        "image_mode": image.mode,
        "info": info,
        }

    await db_client.db['images'].update_one({'_id': ObjectId(id)}, {'$set': image_dict})

    # save image to local storage. then close file pointer to image 
    image.save(file_path)
    image.close()

"""Utilities for file reading & writing operations
"""
from fastapi import UploadFile
from uuid import uuid4
from config.setup import settings
from os import path, mkdir


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

    # write file to local storage
    with open(file_path, 'wb') as local_file:
        local_file.write(file_buffer)

    return file_path

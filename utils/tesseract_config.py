"""Utilities for tesseract configuration & options
"""
from db.mongodb import db_client
from models.tesseract import TesseractConfigModel


async def background_setup_tess_config(tess_req_dict: dict) -> dict:
    """Based on tesseract configuration parameters passed in request,
    preapares a TesseractConfigurationModel, and return it as dict."""

    # check if a TesseractConfigModel already exist in db for given params
    config_dict = await db_client.db['tess_config'].find_one(tess_req_dict)

    # if no TesseractConfigModel exist in db, create one
    if config_dict is None:
        tess_config = TesseractConfigModel(**tess_req_dict)
        # dump model to dict excluding `id` (None)
        config_dict = tess_config.model_dump(exclude=['id'])

        # insert in db & assign id to config dict
        insert_result = await db_client.db['tess_config'].insert_one(config_dict)
        config_dict['id'] = insert_result.inserted_id
    else:
        # if returned from db, set `id`
        config_dict['id'] = config_dict['_id']
    return config_dict

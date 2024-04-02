"""Utilities for tesseract tesseract related operations
"""
import asyncio
import pytesseract as pts
from db.mongodb import db_client
from concurrent.futures import ThreadPoolExecutor
from config.setup import settings
from models.tesseract import TesseractConfigModel, TesseractOutputModelImage,\
    TesseractOutputModelPdf
from PIL.Image import Image
from typing import List, Tuple
import time


def parse_ocr_result(result_dict: dict) -> Tuple[str, float]:
    """
    Extracts OCR result text and accuracy from OCR result dict.

    Args:
        result_dict (dict): A dictionary containing detailed OCR result.
        Contains information about recognized words location in the input
        image and the confidence they are recognized with. Keys in dict:
        [`level`, `page_num`, `block_num`, `par_num`, `line_num`, `word_num`,
        `left`, `top`,  `width`, `height`, `conf` and `text`].

    Returns:
        (tuple[str, float]): a tuple of ocr result text and average confidence
    """
    # get indices of paragraphs, lines and words (levels 4 & 5)
    word_line_par_indces = [
        i for i in range(len(result_dict['level']))
        if result_dict['level'][i] in (3, 4, 5)
    ]

    ocr_result_text = ''
    confidence_sum = 0
    total_words = 0
    # concatenate strings & find mean confidence
    for i in word_line_par_indces:
        if result_dict['level'][i] in (3, 4):
            # add newline for lines & paragraphs
            if not ocr_result_text.endswith('\n\n'):
                ocr_result_text += '\n'
        else:
            # add space b/n words (while skipping space words)
            if not result_dict['text'][i].isspace():
                ocr_result_text += result_dict['text'][i] + ' '
                confidence_sum += result_dict['conf'][i]
                total_words += 1

    if total_words != 0:
        mean_confidence = round(confidence_sum / total_words, 2)
    else:   # no words recognized (one cause: misconfiguration of tesseract)
        mean_confidence = 0

    return ocr_result_text, mean_confidence


async def background_setup_tess_config(tess_req_dict: dict) -> dict:
    """
    Based on tesseract configuration parameters passed in request,
    preapares a TesseractConfigurationModel, and returns it as dict.
    """
    # default tesseract CONFIGVARS (to be passed using -c)
    # TODO: move `default_config_vars` to a TesseractSettings class in config
    default_config_vars = {
        'load_system_dawg': 0,
        'load_freq_dawg': 0,
        'textord_space_size_is_variable': 1,
        'preserve_interword_spaces': 1
        }

    # set CONFIGVARs in tess_req_dict with default values (if not set already)
    tess_req_dict['config_vars'].update(
        {k: v for k, v in default_config_vars.items()
         if k not in tess_req_dict['config_vars']})

    # sort items in the nested dictionary `config_vars` since mongodb uses
    # field order in nested documents (dicts) for equality matches
    tess_req_dict['config_vars'] = dict(
        sorted(tess_req_dict['config_vars'].items()))

    # check if a TesseractConfigModel already exist in db for given params
    config_dict = await db_client.db.tess_config.find_one(tess_req_dict)

    # if no TesseractConfigModel exist in db, create one
    if config_dict is None:
        tess_config = TesseractConfigModel(**tess_req_dict)
        # dump model to dict excluding `id` (None)
        config_dict = tess_config.model_dump(exclude={'id'})

        # insert in db & assign id to config dict
        insert_result = await db_client.db.tess_config.insert_one(config_dict)
        config_dict['id'] = insert_result.inserted_id
    else:
        # if returned from db, set `id`
        config_dict['id'] = config_dict['_id']

    return config_dict


OCR_IN_PROGRESS: int = 0
"""Keeps track of no. of images being processed"""


async def background_run_tesseract_image(
        image: Image, image_id: str, tess_config_dict: dict):
    """
    Runs tesseract in a ThreadPool and returns the result.

    Args:
        image (Image): image loaded using PIL
        image_id (str): id of image in database
        tess_config_dict (dict): tesseract configuration dictionary

    Returns:
        (dict): a dictionary with information about ocr process and result.
    """
    # set as global (otherwise UnboundLocalError: referenced before assignment)
    global OCR_IN_PROGRESS

    # set tesseract config string from config_dict
    config = '-l {} --psm {} --oem {}'.format(
        tess_config_dict['language'],
        tess_config_dict['psm'],
        tess_config_dict['oem'])

    for key, value in tess_config_dict['config_vars'].items():
        config += ' -c {}={}'.format(key, value)

    # get the running event loop in the current OS thread
    # [REFERENCE](https://docs.python.org/3.8/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)  # noqa
    loop = asyncio.get_running_loop()

    # run tesseract OCR in a custom thread pool. Increase workers if available.
    # (Better efficieny than ProcessPoolExecutor)
    with ThreadPoolExecutor(max_workers=settings.OCR_WORKERS) as pool:
        # before running OCR on a new image, wait for previous one to finish.
        # if added immediately, executor won't return until all images are done
        while OCR_IN_PROGRESS > 0:
            await asyncio.sleep(2)  # TODO: check d/t sleep durations effect

        OCR_IN_PROGRESS = OCR_IN_PROGRESS + 1

        # set start benchmark time
        start = time.perf_counter()

        ocr_result_dict = await loop.run_in_executor(
            pool,
            lambda: pts.image_to_data(
                image, config=config, output_type=pts.Output.DICT
                )
            )

        # set time taken (TODO: use other counters & check d/ce)
        time_taken = time.perf_counter() - start

        image.close()   # as precaution (side effect not clear if not closed)

        OCR_IN_PROGRESS = OCR_IN_PROGRESS - 1

    # parse result dict and get text and accuracy
    ocr_result_text, ocr_accuracy = parse_ocr_result(ocr_result_dict)

    # create a TesseractOutputModel for this image OCR
    tess_output_dict = {
        'image_id': image_id,
        'tess_config_id': tess_config_dict['id'],
        'time_taken': time_taken,
        'ocr_accuracy': ocr_accuracy,
        'ocr_result_text': ocr_result_text,
        'ocr_result_dict': ocr_result_dict,
    }

    tess_output = TesseractOutputModelImage(**tess_output_dict)

    # save output model in db
    tess_output_dict = tess_output.model_dump(exclude={'id'})
    insert_result = await db_client.db.tess_output.insert_one(tess_output_dict)

    tess_output_dict['id'] = insert_result.inserted_id

    return tess_output_dict


async def background_run_tesseract_pdf(
        pdf_images: List[Image], pdf_id: str, tess_config_dict: dict):
    """
    Runs tesseract in a ThreadPool and returns the result.

    Args:
        pdf_images (List[Image]): list of pdf pages loaded as PIL image.
        pdf_id (str): id of pdf in database
        tess_config_dict (dict): tesseract configuration dictionary

    Returns:
        (dict): a dictionary with information about ocr process and result.
    """
    # set as global (otherwise UnboundLocalError: referenced before assignment)
    global OCR_IN_PROGRESS

    # set tesseract config string from config_dict
    config = '-l {} --psm {} --oem {}'.format(
        tess_config_dict['language'],
        tess_config_dict['psm'],
        tess_config_dict['oem'])

    for key, value in tess_config_dict['config_vars'].items():
        config += ' -c {}={}'.format(key, value)

    # get the running event loop in the current OS thread
    # [REFERENCE](https://docs.python.org/3.8/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)  # noqa
    loop = asyncio.get_running_loop()

    # run tesseract OCR in a custom thread pool. Increase workers if available.
    # (Better efficieny than ProcessPoolExecutor)
    with ThreadPoolExecutor(max_workers=settings.OCR_WORKERS) as pool:
        # a dictionary to store ocr results for each page
        pages_ocr_result = {
            'time_taken': {}, 'ocr_result_text': {},
            'ocr_result_dict': {}, 'ocr_accuracy': {}
            }

        for i, image in enumerate(pdf_images):
            # before running OCR on a new image, wait for previous one to finish.
            # if added immediately, executor won't return until all images are done
            while OCR_IN_PROGRESS > 0:
                await asyncio.sleep(2)  # TODO: check d/t sleep durations effect

            OCR_IN_PROGRESS = OCR_IN_PROGRESS + 1

            # set start benchmark time
            start = time.perf_counter()

            ocr_result_dict = await loop.run_in_executor(
                pool,
                lambda: pts.image_to_data(
                    image, config=config, output_type=pts.Output.DICT
                    )
                )

            # set time taken (TODO: use other counters & check d/ce)
            time_taken = time.perf_counter() - start

            image.close()   # as precaution (side effect not clear if not closed)

            OCR_IN_PROGRESS = OCR_IN_PROGRESS - 1

            # parse result dict and get text and accuracy
            ocr_result_text, ocr_accuracy = parse_ocr_result(ocr_result_dict)

            # store each pages result
            pages_ocr_result['time_taken'][str(i + 1)] = time_taken
            pages_ocr_result['ocr_accuracy'][str(i + 1)] = ocr_accuracy
            pages_ocr_result['ocr_result_text'][str(i + 1)] = ocr_result_text
            pages_ocr_result['ocr_result_dict'][str(i + 1)] = ocr_result_dict

    # create a TesseractOutputModelPdf for this pdf OCR
    pdf_tess_output_dict = {
        'pdf_id': pdf_id,
        'tess_config_id': tess_config_dict['id'],
        'time_taken': pages_ocr_result['time_taken'],
        'ocr_accuracy': pages_ocr_result['ocr_accuracy'],
        'ocr_result_text': pages_ocr_result['ocr_result_text'],
        'ocr_result_dict': pages_ocr_result['ocr_result_dict'],
    }

    tess_output = TesseractOutputModelPdf(**pdf_tess_output_dict)

    # save output model in db
    tess_output_dict = tess_output.model_dump(exclude={'id'})
    insert_result = await db_client.db.tess_output.insert_one(tess_output_dict)

    tess_output_dict['id'] = insert_result.inserted_id

    return tess_output_dict
"""Image OCR using pytesseract
"""
from bson import ObjectId
from datetime import datetime, timezone
from db.mongodb import db_client
from utils.file_read_write import background_write_file_pdf,\
    background_write_ocr_result_pdf
from utils.tesseract import background_setup_tess_config,\
    background_run_tesseract_pdf


async def background_pdf_ocr(
    file_buffer: bytes, pdf_dict: dict, tess_req_dict: dict
):
    """Performs OCR on a pdf using background tasks.

    Args:
        file_buffer (bytes): uploaded pdf as bytes
        pdf_dict (dict): dictionary dump of pdf in database
        tess_req_dict (dict): tesseract configuration parameters passed
            in request body
    """
    # get tesseract configuration based on given params in request
    tess_config_dict = await background_setup_tess_config(tess_req_dict)
    print('Tesseract: CONFIGURED')

    # save pdf in local storage & get pdf_dict (metadata & storage path)
    pdf_images, pdf_update_dict = await background_write_file_pdf(
        file_buffer, pdf_dict['name']
    )
    print('Image: WRITTEN 2 LOCAL')

    # run tesseract in background & get output model dict & result text
    tess_output_dict = await background_run_tesseract_pdf(
        pdf_images, pdf_dict['id'], tess_config_dict
    )
    print('Tesseract: OCR FINISHED')

    # add `str` output format to `done_output_formats`
    pdf_update_dict['done_output_formats'] = {
        'str': 'Set to Pdfs `ocr_result_text` field.'
    }

    # if str is not in output file formats list add it (default)
    if 'str' not in pdf_dict['ocr_output_formats']:
        pdf_dict['ocr_output_formats'].append('str')
        # add it to update_dict also (to update pdf in db)
        pdf_update_dict['ocr_output_formats'] = pdf_dict[
            'ocr_output_formats']

    # write OCR result to file (text, word or pdf)
    if any([fmt in pdf_dict['ocr_output_formats']
            for fmt in ('txt', 'docx', 'pdf')]):

        # write files and get their path
        write_ocr_result_dict = await background_write_ocr_result_pdf(
            pdf_update_dict['local_path'], pdf_dict, tess_output_dict
        )
        print(f"Result Saved in {list(write_ocr_result_dict.keys())} formats")

        # add saved outptut formats to `done_output_formats`.
        pdf_update_dict['done_output_formats'].update(write_ocr_result_dict)

    # update pdf in db
    pdf_update_dict.update({
        'ocr_finished': True,
        'ocr_result_text': tess_output_dict['ocr_result_text'],
        'ocr_accuracy': tess_output_dict['ocr_accuracy'],
        'tess_output_id': tess_output_dict['id'],
        "tess_config_id": tess_config_dict['id'],
        'updated_at': datetime.now(timezone.utc)
    })

    await db_client.db.pdfs.update_one(
        {'_id': ObjectId(pdf_dict['id'])},
        {'$set': pdf_update_dict},
        True   # upsert=True (update nested docs too. else replace inner docs.)
    )

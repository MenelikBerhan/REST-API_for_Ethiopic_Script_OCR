"""Image endpoints
"""
from db.mongodb import db_client
from fastapi import APIRouter, BackgroundTasks, Body, File, status, UploadFile
from models.pdfs import PdfModel, PdfCollection, PdfPostRequestModel,\
    PdfPostResponseModel
from models.tesseract import TesseractConfigRequestModel
from ocr.pdf_ocr import background_pdf_ocr


# create a router with `/pdf` prefix
pdf_router = APIRouter(prefix='/pdf')


@pdf_router.get(
    '/',
    response_description='__List of all pdfs__',
    response_model=PdfCollection,
    response_model_by_alias=False,
    response_model_exclude_none=True,
    tags=['PDF']
)
async def list_pdfs():
    """
    ### List all of the pdfs in the database.

    ### The response is unpaginated and limited to 50 results.
    """
    return PdfCollection(pdfs=await db_client.db.pdfs.find().to_list(50))


# Content-type will be multipart/form-data, `pdf_properties` is a stringfied
# dict which will be converted to dict in `PdfRequestBody` before validation.
# [Reference](https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request/70640522#70640522)
@pdf_router.post(
    '/',
    response_description='__Created pdf__',
    response_model=PdfPostResponseModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_model_exclude_none=True,
    tags=['PDF']
)
async def create_pdf(
    background_tasks: BackgroundTasks,
    pdf_properties: PdfPostRequestModel = Body(default=None),
    tesseract_config: TesseractConfigRequestModel = Body(default=None),
    file: UploadFile = File(
        ...,
        description="""__Pdf file containing images (MAX 178956970 pixels)
        to be OCR'ed__"""
    )
):
    """
    ### Insert a new pdf record into the database, save pdf in local\
    storage and perform OCR in the background.
    """
    # space in pdf files replaced by `_`
    file_name = file.filename.replace(' ', '_')

    # name of uploaded pdf (for db)
    pdf_dict = {'name': file_name}

    # add fields set in request body to pdf_dict.
    if pdf_properties:
        pdf_dict.update(
            pdf_properties.model_dump(exclude_none=True))

    # create a PdfModel using pdf_dict
    pdf = PdfModel(**pdf_dict)

    # create a dict for db excluding `id` (default=None). To avoid saving
    # null & unset fields in db, use (exclude_unset=True, exclude_none=True)
    new_pdf_dict = pdf.model_dump(exclude=['id'])

    # insert the new pdf in db
    insert_result = await db_client.db.pdfs.insert_one(new_pdf_dict)

    # add id generated by mongodb to pdf attributes and return new pdf
    new_pdf_dict['id'] = insert_result.inserted_id

    # get a dictionary of tesseract params from request body
    tess_req_dict = tesseract_config.model_dump()

    # read file into buffer & pass buffer to background tasks.
    # can't pass file directly, it is closed before processing.
    file_buffer = await file.read()

    # as a precaution close file. (FastApi closes it after sending response)
    await file.close()

    # add a background task to OCR the pdf
    background_tasks.add_task(
        background_pdf_ocr,
        file_buffer,
        new_pdf_dict,
        tess_req_dict,
    )

    return new_pdf_dict

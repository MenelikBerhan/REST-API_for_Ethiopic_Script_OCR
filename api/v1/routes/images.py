'''Image endpoints
'''
from fastapi import APIRouter
from db.mongodb import db_client
from models.images import ImageModel, ImageCollection
from fastapi import Body, status


# create a router with `/images` prefix
image_router = APIRouter(prefix='/images')


@image_router.get(
    '/',
    response_description='List all images',
    response_model=ImageCollection,
    response_model_by_alias=False,
)
async def list_images():
    """
    List all of the images in the database.

    The response is unpaginated and limited to 50 results.
    """
    return ImageCollection(images=await db_client.db['images'].find().to_list(50))


@image_router.post(
    '/',
    response_description='Add new image',
    response_model=ImageModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_image(image: ImageModel = Body(...)):
    """
    Insert a new image record in to the database.   
    """
    # don't use any given id, and create a dict for db using alias `_id`.
    # To handle given id, add ObjectId validation and remove `exclude=['id']`
    image_dict = image.model_dump(by_alias=True, exclude=['id'])

    # insert the new image in db
    new_image = await db_client.db['images'].insert_one(image_dict)

    # add id generated by mongodb to image attributes and return new image
    image_dict['id'] = new_image.inserted_id
    return image_dict
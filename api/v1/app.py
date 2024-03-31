"""Entry point for API
"""
from config.setup import settings
from db.mongodb import db_client
from fastapi import FastAPI
from api.v1.routes.images import image_router
from api.v1.routes.ocr import ocr_router
import uvicorn

# create fastapi app
app = FastAPI(
    debug=settings.APP_DEBUG_MODE,
    title=settings.APP_TITLE,
    summary=settings.APP_SUMMARY,
    description=settings.APP_DESCRIPTION
    )


# connect & disconnect dbclient on app startup & shutdown
app.add_event_handler('startup', db_client.connect)
app.add_event_handler('shutdown', db_client.disconnect)

# include routers in to the app
app.include_router(image_router)
app.include_router(ocr_router)


if __name__ == '__main__':
    # start uvicorn server
    uvicorn.run(
        'api.v1.app:app',
        host=settings.SERVER_HOST,
        reload=settings.SERVER_RELOAD,
        port=settings.SERVER_PORT,
    )

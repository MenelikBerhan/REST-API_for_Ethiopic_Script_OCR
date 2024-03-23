"""Entry point for API
"""
from config.setup import settings
from db.mongodb import db_client
from fastapi import FastAPI
from api.v1.routes.images import image_router
import uvicorn

# create fastapi app
app = FastAPI(
    debug=settings.DEBUG_MODE,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    description=settings.DESCRIPTION
    )


# connect & disconnect dbclient on app startup & shutdown
app.add_event_handler('startup', db_client.connect)
app.add_event_handler('shutdown', db_client.disconnect)

# include routers in to the app
app.include_router(image_router)


if __name__ == '__main__':
    # start uvicorn server
    uvicorn.run(
        'api.v1.app:app',
        host=settings.HOST,
        reload=settings.RELOAD,
        port=settings.PORT,
    )

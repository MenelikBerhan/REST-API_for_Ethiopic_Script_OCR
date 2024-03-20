"""Entry point for API
"""
from fastapi import FastAPI
from config.setup import settings
from db.mongodb import db_client
import uvicorn

app = FastAPI(
    debug=settings.DEBUG_MODE,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    description=settings.DESCRIPTION)


# connect & disconnect dbclient on app startup & shutdown
app.add_event_handler('startup', db_client.connect)
app.add_event_handler('shutdown', db_client.disconnect)


if __name__ == "__main__":
    print(settings.DEBUG_MODE)
    uvicorn.run(
        'api.v1.app:app',
        host=settings.HOST,
        reload=settings.RELOAD,
        port=settings.PORT,
    )

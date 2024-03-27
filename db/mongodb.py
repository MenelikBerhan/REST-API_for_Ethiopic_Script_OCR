"""Mongodb database client
"""
from config.setup import settings
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase
from typing import Union


class DbClient:
    """A mongodb database connection client."""
    def __init__(self):
        """Initialize instance"""
        self.url = f'mongodb://{settings.DB_HOST}:{settings.DB_PORT}'
        self.client: AgnosticClient
        self.db: AgnosticDatabase

    async def connect(self):
        """Establishes mongodb connection on app startup."""
        print("Connecting to mongodb database")
        # create a mongodb client & database
        self.client = AsyncIOMotorClient(self.url)
        self.db = self.client[settings.DB_NAME]

    async def disconnect(self):
        """Closes mongodb connection on app shutdown."""
        print("Closing connection to mongodb database")
        self.client.close()

db_client = DbClient()

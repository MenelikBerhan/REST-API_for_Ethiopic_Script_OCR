"""Setup DB, Server and App settings
"""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# load env variables from .env file
load_dotenv()


# class attributes will be read from env variables of same name
class AppSettings(BaseSettings):
    """For app settings to be set in FastApi."""
    APP_TITLE: str
    APP_SUMMARY: str
    APP_DESCRIPTION: str
    APP_DEBUG_MODE: bool
    OCR_WORKERS: int
    TESSDATA_PREFIX: str


class ServerSettings(BaseSettings):
    """For uvicorn server settings."""
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_RELOAD: bool


class DbSettings(BaseSettings):
    """For mongodb client settings."""
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int


class FileSettings(BaseSettings):
    """For file reading & writing operations."""
    STORAGE_PATH: str


class Settings(AppSettings, ServerSettings, DbSettings, FileSettings):
    """Container for all settings."""
    pass


settings = Settings(_env_file='.env')

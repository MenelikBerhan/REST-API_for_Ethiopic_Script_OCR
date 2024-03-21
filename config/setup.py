"""Setup DB, Server and App settings
"""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# load env variables from .env file
load_dotenv()


# class attributes will be read from env variables of same name
class AppSettings(BaseSettings):
    """For app settings to be set in FastApi."""
    # set prefix to match env variables (APP_TITLE ...)
    model_config = SettingsConfigDict(
        env_prefix='APP_',
        env_ignore_empty=True,
        )

    TITLE: str = "REST-API for Ethiopic Script OCR"
    SUMMARY: str = "An OCR app for Images & PDFs containing Ethiopic Script."
    # TODO add details in description
    DESCRIPTION: str = ""
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    """For uvicorn server settings."""
    model_config = SettingsConfigDict(
        env_prefix='SERVER_',
        env_ignore_empty=True,
        )
    HOST: str = 'localhost'
    PORT: int = 8000
    RELOAD: bool = True


class DbSettings(BaseSettings):
    """For mongodb client settings."""
    model_config = SettingsConfigDict(env_ignore_empty=True)
    DB_NAME: str = 'test'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 27017


class FileSettings(BaseSettings):
    """For file reading & writing operations."""
    model_config = SettingsConfigDict(env_ignore_empty=True)
    STORAGE_PATH: str = '/tmp/ocr_app/'


class Settings(AppSettings, ServerSettings, DbSettings, FileSettings):
    """Container for all settings."""
    pass


settings = Settings()

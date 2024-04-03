"""Setup DB, Server and App settings
"""
from pydantic_settings import BaseSettings


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


class AuthSettings(BaseSettings):
    """For user authentication"""
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTH_SECRET_KEY: str
    """use `openssl rand -hex 32` to generate key."""
    AUTH_ALGORITHM: str


class Settings(
    AppSettings, ServerSettings, DbSettings, FileSettings, AuthSettings
        ):
    """Container for all settings."""
    pass


settings = Settings(_env_file='config/app_env')

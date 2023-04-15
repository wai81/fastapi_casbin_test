import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl

env_path = Path('') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_TITLE: str = "GrkAPI"
    PROJECT_VERSION: str = "0.0.1"

    # API_V1_STR: str = "/api/v1"
    API_V1_STR: str = ""
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8



    # подключения к базе

    dbusername: str = os.getenv("DB_USERNAME")
    password: str = os.getenv("DB_PASSWORD")
    database: str = os.getenv("DB_DATABASE")
    host: str = os.getenv("DB_HOST")
    port: str = os.getenv("DB_PORT")

    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PW: str = "qwerty12"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:4200",
        "http://localhost:8001"  # type: ignore
     ]
    # class Config:
    #     env_prefix = "DB_"
    #     env_file = "../../../.env"


settings = Settings()

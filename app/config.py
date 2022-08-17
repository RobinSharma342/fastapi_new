from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str 
    DATABASE_PASSWORD: str 
    DATABASE_PORT: str 
    DATABASE_NAME: str 
    DATABASE_USERNAME: str 
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ALGORITHM_EXPIRE_MINUTE: int

    class Config:
        env_file = 'app/.env'


@lru_cache()
def get_settings():
    settings = Settings()
    return settings

settings = get_settings()



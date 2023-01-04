from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    jwt_secret: str = Field(..., env='secret')
    jwt_algorithm: str = Field(..., env='algorithm')
    sqlalchemy_url: str = Field(..., env='SQLALCHEMY_URL')
    redis_url: str = Field(..., env='LOCAL_REDIS_URL')
    max_assigned: str = Field(..., env='MAX_ASSIGNED')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
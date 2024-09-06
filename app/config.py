from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_name_test: str
    database_username: str
    redis_hostname: str
    redis_port: str
    redis_db: str
    
    class Config:
        env_file = ".env"
    
settings = Settings()
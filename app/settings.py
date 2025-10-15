from pydantic_settings import BaseSettings  
from typing import Optional
from decouple import config


class Settings(BaseSettings):
    """Application settings"""
    OPENAI_API_KEY: str = config("OPENAI_API_KEY")
    PROJECT_NAME: str = config("PROJECT_NAME", default="DocuMind")
    VERSION: str = config("VERSION", default="1.0.0")
    LLM_MODEL: str = config("LLM_MODEL", default="gpt-3.5-turbo")
    CHUNK_SIZE: int = config("CHUNK_SIZE", default=500, cast=int)
    CHUNK_OVERLAP: int = config("CHUNK_OVERLAP", default=50, cast=int)
    ALLOWED_ORIGINS: Optional[str] = config("ALLOWED_ORIGINS", default="*")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

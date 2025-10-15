from decouple import config


class Config:
    APP_NAME = "DocuMind"
    VERSION = config("VERSION", default="0.1.0")
    DATABASE_URL = config("DATABASE_URL", default="sqlite:///./test.db")
    LLM_API_KEY = config("LLM_API_KEY", default="")

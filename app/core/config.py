import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Get the env vaiables from .env (for local dev)
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SECRET_KEY = os.getenv("DB_SECRET_KEY")


class Settings(BaseSettings):
    # Try reading DATABASE_URL, etc.. (for Docker), if not present use fallback values (for localhost)
    DATABASE_URL: str = (
        open("/run/secrets/database_url").read().strip()
        if os.path.exists("/run/secrets/database_url")
        else os.getenv(
            "DATABASE_URL",
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        )
    )
    SECRET_KEY: str = (
        open("/run/secrets/secret_key").read().strip()
        if os.path.exists("/run/secrets/secret_key")
        else os.getenv("SECRET_KEY", DB_SECRET_KEY)
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()

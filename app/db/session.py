from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


# Get the env vaiables from .env (for local dev)
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Try reading DATABASE_URL (for Docker), if not present use fallback values (for localhost)
DATABASE_URL = (
    open("/run/secrets/database_url").read().strip()
    if os.path.exists("/run/secrets/database_url")
    else os.getenv(
        "DATABASE_URL",
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

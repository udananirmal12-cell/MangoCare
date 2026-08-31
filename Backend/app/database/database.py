import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# --------------------------------------------------
# MySQL connection URL
# --------------------------------------------------

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)


# --------------------------------------------------
# SQLAlchemy engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# --------------------------------------------------
# Database session
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# --------------------------------------------------
# FastAPI database dependency
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
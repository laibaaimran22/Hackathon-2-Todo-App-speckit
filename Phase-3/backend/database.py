from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Remove quotes if they exist around the URL (handles various quote scenarios)
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.strip()  # Remove leading/trailing whitespace
    # Remove surrounding quotes (single or double)
    if (DATABASE_URL.startswith('"') and DATABASE_URL.endswith('"')) or \
       (DATABASE_URL.startswith("'") and DATABASE_URL.endswith("'")):
        DATABASE_URL = DATABASE_URL[1:-1]
    # Also handle case where only leading quote exists
    if DATABASE_URL.startswith('"') or DATABASE_URL.startswith("'"):
        DATABASE_URL = DATABASE_URL[1:]
    if DATABASE_URL.endswith('"') or DATABASE_URL.endswith("'"):
        DATABASE_URL = DATABASE_URL[:-1]
    # Strip again after quote removal
    DATABASE_URL = DATABASE_URL.strip()

# Neon requires SSL for connections - configure pool and SSL settings
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=300,     # Recycle connections after 5 minutes
    pool_size=5,
    max_overflow=10,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
    }
)

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        raise

from contextlib import contextmanager
from typing import Generator

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

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
        # Create only our custom tables (not the auth tables which are managed by Better Auth)
        # First, create all tables that don't exist yet
        from models import Task, User, Tag, TaskTagLink
        SQLModel.metadata.create_all(engine, checkfirst=True)

        # Add missing columns to existing task table if they don't exist
        from sqlalchemy import text
        with engine.connect() as conn:
            try:
                # Check if priority column exists, if not add it
                result = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'task' AND column_name = 'priority'
                """))
                if not result.fetchone():
                    conn.execute(text("ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium'"))
                    print("Added priority column to task table")

                # Check if due_date column exists, if not add it
                result = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'task' AND column_name = 'due_date'
                """))
                if not result.fetchone():
                    conn.execute(text("ALTER TABLE task ADD COLUMN due_date TIMESTAMP WITH TIME ZONE"))
                    print("Added due_date column to task table")

                # Check if recurrence_pattern column exists, if not add it
                result = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'task' AND column_name = 'recurrence_pattern'
                """))
                if not result.fetchone():
                    conn.execute(text("ALTER TABLE task ADD COLUMN recurrence_pattern VARCHAR(50)"))
                    print("Added recurrence_pattern column to task table")

                conn.commit()
            except Exception as e:
                print(f"Error modifying task table: {str(e)}")
                # If we can't modify the table, just continue and hope the basic tables work

        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        raise

from contextlib import contextmanager
from typing import Generator

def get_session():
    with Session(engine) as session:
        yield session

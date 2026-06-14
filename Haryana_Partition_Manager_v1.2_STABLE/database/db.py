from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
)

from database.models import Base


# =====================================
# DATABASE PATH
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    exist_ok=True
)

DATABASE_FILE = (
    DATA_DIR / "haryana.db"
)

DATABASE_URL = (
    f"sqlite:///{DATABASE_FILE}"
)


# =====================================
# ENGINE
# =====================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)


# =====================================
# SESSION FACTORY
# =====================================

SessionLocal = scoped_session(

    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine
    )
)


# =====================================
# CREATE DATABASE
# =====================================

def create_database():

    Base.metadata.create_all(
        bind=engine
    )


# =====================================
# GET SESSION
# =====================================

def get_session():

    return SessionLocal()


# =====================================
# CLOSE SESSION
# =====================================

def close_session(session):

    try:
        session.close()

    except Exception:
        pass
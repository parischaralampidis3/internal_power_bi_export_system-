from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/power_bi_export_system.db.sqlite3"

engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread":True}
)

"""
Why echo=False?

echo=True = Print every SQL query to console (useful for debugging)
echo=False = Quiet mode (production-like)
You can change this to True later if queries seem wrong
"""

SessionLocal = sessionmaker(autocommit=False, autoFlush =False, bind = engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
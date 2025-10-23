from sqlmodel import SQLModel, create_engine, Session
from .config import settings
import urllib.parse

# If using SQLite, set connect_args to avoid check_same_thread errors when
# the engine is used from multiple threads (uvicorn workers/threads).
if settings.DATABASE_URL.startswith("sqlite"):
    # For file URLs like sqlite:///./gymai.db SQLAlchemy handles them directly.
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(settings.DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

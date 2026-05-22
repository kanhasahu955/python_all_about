from sqlmodel import Session, SQLModel, create_engine

from core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=settings.DEBUG,
)


def init_db() -> None:
    """Create database tables from registered SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

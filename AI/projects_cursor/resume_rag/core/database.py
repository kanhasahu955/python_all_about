from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)

def create_db_and_tables():
    from projects_cursor.resume_rag.models.resume_model import ResumeDocument, ResumeAnalysis
    from projects_cursor.resume_rag.models.datasource_model import DataSource
    from projects_cursor.resume_rag.models.job_model import BackgroundJob

    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
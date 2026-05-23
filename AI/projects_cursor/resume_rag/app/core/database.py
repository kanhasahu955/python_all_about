from sqlmodel import SQLModel, Session, create_engine

from app.core.config import DBProvider, settings

_engine_kwargs: dict = {
    "echo": False,
    "pool_pre_ping": True,
}

if settings.DB_PROVIDER == DBProvider.snowflake:
    _engine_kwargs["connect_args"] = {"client_session_keep_alive": True}

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)


def create_db_and_tables():
    from app.models.agent_model import AgentRun  # noqa: F401
    from app.models.datasource_model import DataSource  # noqa: F401
    from app.models.job_model import BackgroundJob  # noqa: F401
    from app.models.resume_model import ResumeAnalysis, ResumeDocument  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

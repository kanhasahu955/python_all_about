from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session, test_connection
from app.core.config import settings
from app.models.datasource_model import DataSource
from app.schemas.datasource_schema import DataSourceCreate, DataSourceTestRequest
from app.services.datasource_service import test_datasource_connection

router = APIRouter()


def _serialize_datasource(ds: DataSource) -> dict:
    return {
        "id": ds.id,
        "name": ds.name,
        "provider": ds.provider,
        "host": ds.host,
        "port": ds.port,
        "database_name": ds.database_name,
        "schema_name": ds.schema_name,
        "warehouse": ds.warehouse,
        "role": ds.role,
        "is_active": ds.is_active,
    }


@router.get("/")
def list_datasources(session: Session = Depends(get_session)):
    rows = session.exec(select(DataSource).where(DataSource.is_active == True)).all()
    return [_serialize_datasource(ds) for ds in rows]


@router.post("/")
def create_datasource(payload: DataSourceCreate, session: Session = Depends(get_session)):
    ds = DataSource(**payload.model_dump())
    session.add(ds)
    session.commit()
    session.refresh(ds)
    return _serialize_datasource(ds)


@router.post("/test")
def test_datasource_config(payload: DataSourceTestRequest):
    return test_datasource_connection(payload)


@router.get("/app-db/test")
def test_app_database():
    ok, err = test_connection()
    return {
        "success": ok,
        "message": "App database connected" if ok else err,
        "provider": settings.DB_PROVIDER.value,
    }


@router.post("/{datasource_id}/test")
def test_datasource(datasource_id: int, session: Session = Depends(get_session)):
    ds = session.get(DataSource, datasource_id)
    if not ds:
        return {"success": False, "message": "Datasource not found"}

    payload = DataSourceTestRequest(
        provider=ds.provider,
        host=ds.host,
        port=ds.port,
        username=ds.username,
        password=ds.password,
        database_name=ds.database_name,
        schema_name=ds.schema_name,
        warehouse=ds.warehouse,
        role=ds.role,
        token=ds.token,
        http_path=ds.http_path,
        catalog=ds.catalog,
    )
    return test_datasource_connection(payload)

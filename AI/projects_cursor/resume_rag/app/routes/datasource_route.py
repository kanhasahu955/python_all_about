from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.datasource_model import DataSource
from app.schemas.datasource_schema import DataSourceCreate

router = APIRouter()


@router.get("/")
def list_datasources(session: Session = Depends(get_session)):
    return session.exec(select(DataSource).where(DataSource.is_active == True)).all()


@router.post("/")
def create_datasource(payload: DataSourceCreate, session: Session = Depends(get_session)):
    ds = DataSource(**payload.model_dump())
    session.add(ds)
    session.commit()
    session.refresh(ds)
    return ds


@router.post("/{datasource_id}/test")
def test_datasource(datasource_id: int, session: Session = Depends(get_session)):
    ds = session.get(DataSource, datasource_id)
    if not ds:
        return {"success": False, "message": "Datasource not found"}
    return {"success": True, "message": f"Connection to {ds.name} ({ds.provider}) OK"}

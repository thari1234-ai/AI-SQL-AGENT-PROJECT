import re

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.services.import_service import import_uploaded_dataset

router = APIRouter(prefix="/explorer", tags=["explorer"])


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    table_name: str | None = Form(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    content = await file.read()
    try:
        return import_uploaded_dataset(
            db,
            filename=file.filename or "dataset.csv",
            content=content,
            user_id=user.id,
            requested_table_name=table_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/tables")
def list_tables(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[dict]:
    query = text(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
    )
    rows = db.execute(query).fetchall()
    return [{"table_name": row[0]} for row in rows]


@router.get("/tables/{table_name}")
def table_details(table_name: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table_name):
        raise HTTPException(status_code=400, detail="Invalid table name")

    columns_query = text(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = :table_name
        ORDER BY ordinal_position;
        """
    )
    sample_query = text(f'SELECT * FROM "{table_name}" LIMIT 10')
    count_query = text(f'SELECT COUNT(*) FROM "{table_name}"')

    columns = [dict(row._mapping) for row in db.execute(columns_query, {"table_name": table_name}).fetchall()]
    sample = [dict(row._mapping) for row in db.execute(sample_query).fetchall()]
    row_count = db.execute(count_query).scalar()

    return {"columns": columns, "row_count": row_count, "sample": sample}

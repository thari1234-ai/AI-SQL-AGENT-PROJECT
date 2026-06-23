from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import QueryHistory, User
from app.schemas.history import QueryHistoryItem
from app.services.export_service import export_csv, export_xlsx

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[QueryHistoryItem])
def list_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[QueryHistory]:
    return (
        db.query(QueryHistory)
        .filter(QueryHistory.user_id == user.id)
        .order_by(QueryHistory.created_at.desc())
        .limit(100)
        .all()
    )


@router.get("/{history_id}", response_model=QueryHistoryItem)
def get_history(history_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> QueryHistory:
    item = (
        db.query(QueryHistory)
        .filter(QueryHistory.id == history_id, QueryHistory.user_id == user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="History item not found")
    return item


@router.get("/{history_id}/export/{fmt}")
def export_history(
    history_id: int,
    fmt: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Response:
    item = (
        db.query(QueryHistory)
        .filter(QueryHistory.id == history_id, QueryHistory.user_id == user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="History item not found")

    data = item.result_json or {}
    columns = data.get("columns", [])
    rows = data.get("rows", [])

    if fmt == "csv":
        return Response(
            content=export_csv(columns, rows),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=query_{history_id}.csv"},
        )
    if fmt == "xlsx":
        return Response(
            content=export_xlsx(columns, rows),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=query_{history_id}.xlsx"},
        )

    raise HTTPException(status_code=400, detail="Supported formats: csv, xlsx")

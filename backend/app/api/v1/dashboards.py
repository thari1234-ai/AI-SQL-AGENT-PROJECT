from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Dashboard, DashboardWidget, User
from app.schemas.dashboard import DashboardCreate, DashboardResponse, WidgetCreate

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


@router.get("", response_model=list[DashboardResponse])
def list_dashboards(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[Dashboard]:
    return db.query(Dashboard).filter(Dashboard.user_id == user.id).order_by(Dashboard.id.desc()).all()


@router.post("", response_model=DashboardResponse)
def create_dashboard(
    payload: DashboardCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Dashboard:
    item = Dashboard(user_id=user.id, name=payload.name, layout_json={"widgets": []})
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/{dashboard_id}/widgets")
def add_widget(
    dashboard_id: int,
    payload: WidgetCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    dashboard = (
        db.query(Dashboard)
        .filter(Dashboard.id == dashboard_id, Dashboard.user_id == user.id)
        .first()
    )
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    widget = DashboardWidget(
        dashboard_id=dashboard.id,
        query_history_id=payload.query_history_id,
        title=payload.title,
        chart_type=payload.chart_type,
        config_json=payload.config_json,
    )
    db.add(widget)
    db.commit()

    return {"status": "ok", "message": "Widget added"}

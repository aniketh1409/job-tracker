from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Application
from .schemas import ApplicationCreate, ApplicationUpdate

def create_application(db: Session, payload: ApplicationCreate) -> Application:
    app = Application(**payload.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

def list_applications(db: Session, status: str | None = None, company: str | None = None) -> list[Application]:
    stmt = select(Application)
    if status:
        stmt = stmt.where(Application.status == status)
    if company:
        stmt = stmt.where(Application.company.ilike(f"%{company}%"))
    return list(db.scalars(stmt.order_by(Application.updated_at.desc())).all())

def get_application(db: Session, app_id: int) -> Application | None:
    return db.get(Application, app_id)

def update_application(db: Session, app: Application, payload: ApplicationUpdate) -> Application:
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(app, k, v)
    db.commit()
    db.refresh(app)
    return app

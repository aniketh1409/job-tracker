from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..db import crud
from ..db.schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("", response_model=ApplicationOut, status_code=201)
def create(payload: ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, payload)

@router.get("", response_model=list[ApplicationOut])
def list_all(
    status: str | None = Query(default=None),
    company: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_applications(db, status=status, company=company)

@router.patch("/{app_id}", response_model=ApplicationOut)
def update(app_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)):
    app = crud.get_application(db, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return crud.update_application(db, app, payload)

@router.get("/next", response_model=dict)
def next_actions(db: Session = Depends(get_db)):
    # Simple logic: follow up if last_contacted or date_applied is >7 days ago and not final status
    apps = crud.list_applications(db)
    followup_cutoff = date.today() - timedelta(days=7)
    final_status = {"offer", "rejected", "withdrawn"}

    followups = []
    interviews = []

    for a in apps:
        if a.status == "interview":
            interviews.append(a)
        if a.status not in final_status:
            ref_date = a.last_contacted or a.date_applied
            if ref_date and ref_date <= followup_cutoff:
                followups.append(a)

    return {
        "followups": [{"id": a.id, "company": a.company, "role": a.role, "status": a.status} for a in followups[:5]],
        "interviews": [{"id": a.id, "company": a.company, "role": a.role, "status": a.status} for a in interviews[:5]],
    }

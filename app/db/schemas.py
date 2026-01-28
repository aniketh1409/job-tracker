from datetime import date, datetime
from pydantic import BaseModel, Field
from app.db.models import AppStatus

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=160)
    link: str | None = Field(default=None, max_length=500)
    status: AppStatus = AppStatus.applied
    date_applied: date | None = None
    last_contacted: date | None = None
    notes: str | None = None

class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=120)
    role: str | None = Field(default=None, min_length=1, max_length=160)
    link: str | None = Field(default=None, max_length=500)
    status: AppStatus | None = None
    date_applied: date | None = None
    last_contacted: date | None = None
    notes: str | None = None

class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    link: str | None
    status: AppStatus
    date_applied: date | None
    last_contacted: date | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

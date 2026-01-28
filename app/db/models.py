import enum
from sqlalchemy import String, Text, Date, DateTime, Enum, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class AppStatus(str, enum.Enum):
    applied = "applied"
    oa = "oa"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    withdrawn = "withdrawn"

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company: Mapped[str] = mapped_column(String(120), index=True)
    role: Mapped[str] = mapped_column(String(160))
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[AppStatus] = mapped_column(Enum(AppStatus), default=AppStatus.applied, index=True)

    date_applied: Mapped[Date | None] = mapped_column(Date, nullable=True)
    last_contacted: Mapped[Date | None] = mapped_column(Date, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

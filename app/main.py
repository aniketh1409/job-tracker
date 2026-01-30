from fastapi import FastAPI
from .db.models import Base
from .db.session import engine
from .routers.applications import router as applications_router
from fastapi.staticfiles import StaticFiles
from .routers.ui import router as ui_router


app = FastAPI(title="Job Tracker API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(ui_router)

# For MVP: create tables on startup (later you can swap to Alembic migrations)
Base.metadata.create_all(bind=engine)

app.include_router(applications_router)

@app.get("/health")
def health():
    return {"ok": True}

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="app/ui"), name="static")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse("app/ui/index.html")

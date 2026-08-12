from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import router
from app.application.site_service import SiteApplicationService
from app.domain.errors import DuplicateSlugError
from app.infrastructure.sqlite_site_repository import SQLiteSiteRepository


WEB_DIST = Path(__file__).resolve().parents[2] / "web" / "dist"
EXPORTS_DIR = Path(__file__).resolve().parents[2] / "exports"
STORAGE_DIR = Path(__file__).resolve().parents[2] / "storage"


def create_app() -> FastAPI:
    app = FastAPI(title="WBS Dev", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.site_service = SiteApplicationService(SQLiteSiteRepository())

    @app.exception_handler(DuplicateSlugError)
    def duplicate_slug_handler(_: Request, exc: DuplicateSlugError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    app.include_router(router, prefix="/api")
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/published", StaticFiles(directory=EXPORTS_DIR), name="published")
    app.mount("/storage", StaticFiles(directory=STORAGE_DIR), name="storage")

    if WEB_DIST.exists():
        assets_dir = WEB_DIST / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/", include_in_schema=False)
        def index() -> FileResponse:
            return FileResponse(WEB_DIST / "index.html")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

from fastapi import APIRouter

from app import __version__
from app.schemas.health import HealthResponse

router = APIRouter(tags=["santé"])


@router.get("/health")
async def health() -> HealthResponse:
    """Vérifie que l'API répond (utilisé par Docker et l'hébergeur)."""
    return HealthResponse(status="ok", version=__version__)

"""Regroupe les routes de l'API versionnée (/api/v1).

Pour ajouter un groupe de routes :
1. créer un fichier dans `app/api/routes/` qui définit un `router` ;
2. l'inclure ci-dessous avec `api_router.include_router(...)`.
"""

from fastapi import APIRouter

api_router = APIRouter()

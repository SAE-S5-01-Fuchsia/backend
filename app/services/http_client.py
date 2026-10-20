"""Client HTTP partagé pour appeler les API externes.

Un seul `httpx.AsyncClient` est créé au démarrage de l'application (voir
`lifespan` dans `app/main.py`) et réutilisé par toutes les requêtes, ce qui
évite de rouvrir une connexion à chaque appel.
"""

from typing import Annotated, Any, cast

import httpx
from fastapi import Depends, Request


def get_http_client(request: Request) -> httpx.AsyncClient:
    return cast(httpx.AsyncClient, request.app.state.http_client)


HttpClient = Annotated[httpx.AsyncClient, Depends(get_http_client)]


async def fetch_json(
    client: httpx.AsyncClient,
    url: str,
    params: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Appelle `url` en GET et renvoie la réponse JSON.

    Lève `httpx.HTTPStatusError` si l'API répond avec un code d'erreur.
    """
    response = await client.get(url, params=params)
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    return data

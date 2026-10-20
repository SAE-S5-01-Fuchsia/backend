"""Exemple de test d'un appel à une API externe, simulé avec respx.

Aucune requête ne part réellement sur Internet : respx intercepte les appels
faits par httpx et renvoie la réponse définie dans le test.
"""

import httpx
import pytest
import respx

from app.services.http_client import fetch_json

URL = "https://api.example.com/items"


@pytest.mark.anyio
@respx.mock
async def test_fetch_json_returns_payload() -> None:
    route = respx.get(URL).mock(return_value=httpx.Response(200, json={"id": 1}))

    async with httpx.AsyncClient() as client:
        data = await fetch_json(client, URL, params={"q": "test"})

    assert data == {"id": 1}
    assert route.calls.last.request.url.params["q"] == "test"


@pytest.mark.anyio
@respx.mock
async def test_fetch_json_raises_on_error_status() -> None:
    respx.get(URL).mock(return_value=httpx.Response(503))

    async with httpx.AsyncClient() as client:
        with pytest.raises(httpx.HTTPStatusError):
            await fetch_json(client, URL)

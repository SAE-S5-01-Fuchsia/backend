from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    # Le bloc `with` déclenche le démarrage (lifespan) de l'application.
    with TestClient(create_app()) as test_client:
        yield test_client


@pytest.fixture
def anyio_backend() -> str:
    # Permet d'écrire des tests asynchrones avec @pytest.mark.anyio.
    return "asyncio"

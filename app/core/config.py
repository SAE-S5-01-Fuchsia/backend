"""Configuration de l'application, lue depuis les variables d'environnement.

Chaque attribut de `Settings` correspond à une variable d'environnement du
même nom en majuscules (ex. `http_timeout` → `HTTP_TIMEOUT`). En local, les
valeurs peuvent être placées dans un fichier `.env` (voir `.env.example`).
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Backend"
    environment: Literal["development", "test", "production"] = "development"

    # Origines autorisées à appeler l'API depuis un navigateur (format JSON).
    # Inutile pour une app mobile native, utile pour la version web d'Expo.
    cors_origins: list[str] = []

    # Délai maximal (en secondes) des appels aux API externes.
    http_timeout: float = 10.0

    @property
    def docs_enabled(self) -> bool:
        """La documentation interactive n'est exposée qu'hors production."""
        return self.environment != "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()

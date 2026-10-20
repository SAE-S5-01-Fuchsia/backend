# Backend Template

Template de backend Python pour les projets du groupe : une API **FastAPI**
prête à l'emploi, avec linter, typage, tests, hooks Git, Docker et workflows
GitHub Actions. C'est l'équivalent, côté serveur, du template Expo du front.

## Prérequis

- [uv](https://docs.astral.sh/uv/getting-started/installation/) : gère la
  version de Python, l'environnement virtuel et les dépendances.
- [Docker](https://docs.docker.com/get-docker/) *(facultatif)* : pour lancer
  l'API dans les mêmes conditions qu'en production.

Vous n'avez pas besoin d'installer Python vous-même : uv télécharge la
version indiquée dans `.python-version` si elle manque.

## Démarrage

1. **Installer les dépendances**

   ```bash
   uv sync
   ```

2. **Installer les hooks Git** (une seule fois après le clone)

   ```bash
   uv run pre-commit install
   ```

3. **Créer le fichier de configuration**

   ```bash
   cp .env.example .env
   ```

4. **Lancer l'API**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

L'API répond sur <http://localhost:8000>. La documentation interactive
(Swagger), générée automatiquement à partir du code, est disponible sur
<http://localhost:8000/docs>.

> **Tester depuis un téléphone** : lancez l'API avec `--host 0.0.0.0` et
> utilisez l'adresse IP locale de votre ordinateur dans l'app
> (`http://192.168.x.x:8000`), pas `localhost`.

### Avec Docker

```bash
docker compose up --build
```

Le code de `app/` est monté dans le conteneur : les modifications sont prises
en compte sans reconstruire l'image.

## Commandes utiles

| Action | Commande |
| --- | --- |
| Lancer l'API en développement | `uv run uvicorn app.main:app --reload` |
| Lancer les tests | `uv run pytest` |
| Tests avec couverture | `uv run pytest --cov --cov-report=term-missing` |
| Vérifier le code (lint) | `uv run ruff check .` |
| Corriger automatiquement | `uv run ruff check --fix .` |
| Formater le code | `uv run ruff format .` |
| Vérifier le typage | `uv run mypy app tests` |
| Ajouter une dépendance | `uv add nom-du-paquet` |
| Ajouter une dépendance de dev | `uv add --dev nom-du-paquet` |

Pensez à commiter `pyproject.toml` **et** `uv.lock` après chaque ajout de
dépendance : le fichier `uv.lock` garantit que tout le monde (et la CI)
utilise exactement les mêmes versions.

## Structure du projet

```
app/
├── main.py              création de l'application (point d'entrée)
├── core/config.py       configuration lue depuis les variables d'environnement
├── api/
│   ├── router.py        regroupe les routes de /api/v1
│   └── routes/          un fichier par groupe de routes
├── schemas/             modèles Pydantic des requêtes et réponses
└── services/            logique métier et appels aux API externes
tests/                   tests (pytest), un fichier par module testé
scripts/                 scripts utilitaires (hook de commit…)
```

- **Les routes** (`api/routes/`) reçoivent les requêtes et renvoient les
  réponses. Elles restent courtes et délèguent le travail aux services.
- **Les services** (`services/`) contiennent la logique et les appels aux API
  externes. Utilisez le client HTTP partagé (`HttpClient`) plutôt que d'en
  créer un nouveau à chaque appel.
- **Les schémas** (`schemas/`) décrivent les données échangées. FastAPI s'en
  sert pour valider les entrées et générer la documentation.

### Ajouter une route

1. Créer `app/api/routes/exemple.py` avec un `router = APIRouter()`.
2. L'inclure dans `app/api/router.py` :
   `api_router.include_router(exemple.router, prefix="/exemple")`.
3. Ajouter les tests correspondants dans `tests/`.

### Ajouter une variable de configuration

1. Ajouter l'attribut dans la classe `Settings` de `app/core/config.py`.
2. Ajouter la variable (sans valeur secrète) dans `.env.example`.
3. La renseigner dans votre `.env` et chez l'hébergeur.

Les secrets (clés d'API…) ne doivent **jamais** être commités, ni placés dans
le code de l'application mobile.

## Développement vs production

- `uv run uvicorn app.main:app --reload` lance l'API en mode développement :
  rechargement automatique, documentation `/docs` active.
- L'image Docker (`Dockerfile`) lance l'API en mode production : sans
  rechargement, sans les dépendances de développement, avec un utilisateur
  non administrateur, et sans la documentation `/docs`.

L'image écoute sur le port défini par la variable `PORT` (8000 par défaut),
fournie automatiquement par la plupart des hébergeurs.

## Workflows GitHub Actions

### 1. CI automatique (`.github/workflows/ci.yml`)

Lancée à chaque push et pull request sur `main` et `develop` :

- vérifie le lint et le formatage (Ruff) ;
- vérifie le typage (Mypy) ;
- lance les tests avec la couverture (Pytest) ;
- vérifie que l'image Docker se construit.

### 2. Build de production (`.github/workflows/build.yml`)

Lancé à chaque merge sur `main`, ou manuellement depuis l'onglet Actions :

- construit l'image Docker de production ;
- la publie dans le registre GitHub (`ghcr.io/<organisation>/<dépôt>`),
  visible dans l'onglet **Packages** de l'organisation ;
- aucun secret à configurer : le workflow utilise le jeton fourni par GitHub.

## Outils utilisés

| Outil | Rôle |
| --- | --- |
| FastAPI | Framework de l'API |
| Uvicorn | Serveur qui exécute l'API |
| Pydantic / pydantic-settings | Validation des données et configuration |
| httpx | Appels aux API externes |
| uv | Dépendances et environnement Python |
| Ruff | Lint et formatage |
| Mypy | Vérification du typage |
| Pytest, respx | Tests et simulation des API externes |
| pre-commit | Hooks Git (lint, typage, message de commit) |
| Docker | Image de production |

Les règles de contribution (branches, commits, pull requests) sont décrites
dans [CONTRIBUTING.md](CONTRIBUTING.md).

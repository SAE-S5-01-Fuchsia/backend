# Guideline du projet

## Convention de nommage et structure

### Fichiers et dossiers

- **Modules et dossiers** : snake_case → `lastfm_service.py`
- **Classes** (dont les schémas Pydantic) : PascalCase → `TrackResponse`
- **Fonctions et variables** : snake_case → `get_top_tracks`
- **Constantes** : MAJUSCULES → `MAX_RESULTS`
- **Tests** : préfixe `test_` → `tests/test_lastfm_service.py`,
  `def test_returns_tracks_sorted_by_playcount()`

### Code

- Toutes les fonctions sont typées (paramètres et retour) : Mypy est en mode
  strict et la CI échoue sinon.
- Les fonctions qui font des appels réseau sont asynchrones (`async def`) et
  utilisent le client HTTP partagé.
- Les tests ne font jamais de vraies requêtes vers Internet : les API externes
  sont simulées avec `respx`.

---

## Workflow Git

N'oubliez pas de vous ajouter dans `.github/CODEOWNERS` pour être associé
automatiquement aux PR.

### Branches

1. **Branches principales**

La branche `main` contient les releases du projet. Chaque merge déclenche le
workflow de build de l'image Docker de production.

La branche `develop` est la branche principale de travail, sur laquelle
toutes les modifications sont mergées. Elle est protégée, tout comme `main`
(cf. Commits).

2. **Branches secondaires**

Toute feature/fix/modification doit faire l'objet d'une branche dédiée, bien
nommée (bon préfixe), puis être mergée sur `develop`.
Les exceptions (modifications directes sur `develop`) sont :
- le changement de version dans `pyproject.toml` et `app/__init__.py` en vue
  d'une release sur `main` ;
- l'édition du `README.md`, du `CONTRIBUTING.md` et du `CODEOWNERS`.

```bash
# Créer une branche pour chaque nouvelle fonctionnalité
git checkout -b feature/nom-de-ta-feature

# Exemples de noms de branches :
# - feature/top-tracks-route
# - fix/itunes-timeout
# - docs/update-readme
```

### Commits

Aucune branche comportant des commits non vérifiés (signés avec une clé SSH
ou GPG) ne peut être mergée sur `develop` ou `main`.

Tout merge doit passer par une PR, qui doit être acceptée par une autre
personne du groupe avant de pouvoir être mergée.

Chaque commit lance automatiquement le linter, le formatage et la
vérification du typage. Si des erreurs sont détectées, le commit est annulé.
Ruff corrige ce qu'il peut tout seul : il suffit alors de refaire
`git add` puis le commit.

### Format autorisé pour les commits

Le format est vérifié automatiquement par le hook `commit-msg`, avec les mêmes
règles que le dépôt front :

- format : `type: description` ;
- la description **commence par une minuscule** ;
- longueur maximale de l'en-tête : **80 caractères** ;
- aucun `scope` n'est autorisé (pas de `type(scope): description`) ;
- types autorisés : `feat`, `fix`, `docs`, `style`, `refactor`, `perf`,
  `test`, `chore`, `ci`.

```
Types :
- feat: nouvelle fonctionnalité
- fix: correction de bug
- docs: documentation
- style: formatage (sans changement de code)
- refactor: refactorisation
- perf: amélioration des performances
- test: ajout ou modification de tests
- chore: maintenance (dépendances, configuration)
- ci: workflows GitHub Actions
```

Exemples valides :

```
feat: ajout de la route des morceaux les plus écoutés
fix: gestion du délai dépassé sur l'api itunes
docs: ajout du guide de contribution
chore: mise à jour des dépendances
```

Exemples invalides :

```
feat(lastfm): ajout de la route      # scope interdit
Fix: correction du cache             # majuscule dans le type
feat: Ajout de la route              # majuscule dans la description
ajout de la route                    # type manquant
```

---

## Avant de push

1. Vérifier que l'API démarre :

   ```bash
   uv run uvicorn app.main:app --reload
   ```

2. Lancer le linter et le formatage :

   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

3. Vérifier le typage :

   ```bash
   uv run mypy app tests
   ```

4. Lancer les tests :

   ```bash
   uv run pytest
   ```

5. Commit et push :

   ```bash
   git add .
   git commit -m "feat: ma nouvelle fonctionnalité"
   git push origin feature/ma-feature
   ```

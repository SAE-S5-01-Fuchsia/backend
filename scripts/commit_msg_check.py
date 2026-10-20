"""Vérifie le format du message de commit (hook commit-msg de pre-commit).

Mêmes règles que le dépôt front (commitlint) :
- format `type: description`, sans scope ;
- types autorisés : feat, fix, docs, style, refactor, perf, test, chore, ci ;
- description qui commence par une minuscule ;
- en-tête de 80 caractères maximum.
"""

import re
import sys
from pathlib import Path

TYPES = ("feat", "fix", "docs", "style", "refactor", "perf", "test", "chore", "ci")
MAX_LENGTH = 80
PATTERN = re.compile(rf"^({'|'.join(TYPES)}): [^A-Z\s].*$")
# Messages générés automatiquement par Git, acceptés tels quels.
IGNORED_PREFIXES = ("Merge ", "Revert ", "fixup! ", "squash! ")


def first_line(message: str) -> str:
    for line in message.splitlines():
        if line.strip() and not line.startswith("#"):
            return line.rstrip()
    return ""


def check(header: str) -> list[str]:
    if header.startswith(IGNORED_PREFIXES):
        return []
    errors = []
    if not PATTERN.match(header):
        errors.append(
            "Le message doit suivre le format `type: description` "
            "(sans scope, description en minuscule)."
        )
    if len(header) > MAX_LENGTH:
        errors.append(
            f"L'en-tête fait {len(header)} caractères (maximum {MAX_LENGTH})."
        )
    return errors


def main() -> int:
    header = first_line(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = check(header)
    if not errors:
        print("✅ Message de commit valide.")
        return 0

    print(f"\n❌ Message de commit refusé : « {header} »\n")
    for error in errors:
        print(f"- {error}")
    print(f"\nTypes autorisés : {', '.join(TYPES)}")
    print("Exemple : feat: ajout de la route des morceaux écoutés")
    print("Voir CONTRIBUTING.md pour plus de détails.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())

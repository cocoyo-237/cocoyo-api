# Convention docstrings — Cocoyo API

Tout le code Python du dépôt suit le style **Google** étendu, rédigé en **français**.

## Périmètre

- Docstring de **module** en tête de chaque fichier `.py`.
- Docstring **complète** sur chaque `def` / `async def` publique.
- Classes Pydantic : docstring de classe + `Field(..., description=...)`.
- Endpoints FastAPI : docstring sur la fonction route (visible dans OpenAPI).

## Sections obligatoires (fonctions métier)

1. Résumé (une ligne)
2. Contexte (module PDF, slice VSA)
3. Préconditions
4. Comportement (étapes numérotées)
5. Règles métier
6. Transactions (ou « N/A »)
7. Args
8. Returns
9. Raises (ou « N/A »)
10. Effets de bord
11. Exemple
12. Voir aussi

Voir l’exemple de référence dans `shared/docstring_examples.py`.

## Outiling

- Ruff `pydocstyle` (Google) configuré en warning dans `pyproject.toml`.
- `tests/test_docstrings.py` vérifie les sections minimales sur les handlers.

# Cocoyo API

API FastAPI (architecture VSA) pour le back-office marque de vêtements : catalogue, commandes, statuts, dashboard.

## Stack

- FastAPI + Pydantic
- Supabase Auth + PostgreSQL (SQLAlchemy async)

## Démarrage

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Renseigner SUPABASE_* et DATABASE_URL
uvicorn main:app --reload
```

Documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger) ou `/redoc`.

1. `POST /auth/login` pour obtenir un `access_token`
2. Bouton **Authorize** → coller le token (sans `Bearer`)
3. Tester les routes protégées

Appliquer `supabase/migrations/00001_initial_schema.sql` sur votre projet Supabase.

## Documentation code

Voir [docs/DOCSTRINGS.md](docs/DOCSTRINGS.md).

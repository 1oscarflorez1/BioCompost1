# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

BioCompost is a university full-stack project (UCC Cali, "Desarrollo Web"): traceability of organic-waste
collection and composting. Three tiers: static frontend (HTML/Bootstrap/vanilla JS) → FastAPI REST API → Oracle
Database via the official `oracledb` driver (thin mode). The course brief requires this stack and the repo layout
(`frontend/`, `backend/`, `database/01-04_*.sql`, `docs/`, `tests/`). Identifiers, routes, comments and UI text
are in Spanish — keep that convention. Keep the code at a clear student level (no ORM, no build step).

## Commands

```bash
docker compose up -d                       # Oracle 23ai Free (reads root .env); wait for "healthy"
cd backend && python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt
python init_db.py                          # drops/recreates tables and loads seed data (database/01-03)
uvicorn main:app --reload                  # API :8000, Swagger at /docs
python -m http.server 5500 --directory frontend   # from repo root; open /login.html
backend/.venv/Scripts/python -m pytest     # from repo root; integration tests need Oracle + seed data
```

## Architecture

- Config comes from the root `.env` (see `.env.example`), loaded in `backend/core/config.py`. No credentials in code.
- `backend/database/connection.py`: oracledb pool + helpers `consultar`, `consultar_uno`, `ejecutar`,
  `insertar` (uses `RETURNING ... INTO`), `clausula_where`. Rows come back as dicts with lowercase keys.
  Always use bind variables; services build optional filters as a list of conditions + params dict
  (oracledb rejects unused bind names).
- Layers: `routers/` (endpoints, HTTP codes, role dependencies in `routers/dependencias.py`) → `services/`
  (business rules + SQL) → `database/`. `schemas/` are Pydantic models (`EsquemaEntrada` turns "" into null,
  `use_enum_values=True`); `models/catalogos.py` holds enums that mirror Oracle CHECK constraints.
- Errors: services raise `core.errores` exceptions (`ReglaNegocio` 400, `NoAutorizado` 401, `Prohibido` 403,
  `NoEncontrado` 404, `Conflicto` 409). Global handlers translate Oracle errors (ORA-00001 → 409, ORA-02292 → 409,
  connection errors → 503) and Pydantic errors (422 with `{detail, errores:[{campo, mensaje}]}`) into Spanish.
  New constraint names need an entry in `DUPLICADOS` / `REGISTROS_ASOCIADOS`.
- Auth: JWT (PyJWT, HS256) + bcrypt. The user is re-read from the DB on every request. `ROLES` has a fixed
  `codigo` (`ADMINISTRADOR` / `RECOLECTOR`, CHECK-constrained) used for all permission checks, and an editable
  display `nombre`. Query results expose `rol` = codigo and `rol_nombre` = nombre; never compare permissions
  against `nombre`. Roles can be renamed (PUT /api/roles/{id}) but not created or deleted.
- Frontend: each page loads `config.js` (API_URL), `auth.js` (Sesion/localStorage), `api.js` (fetch wrapper,
  401 → logout), `ui.js` (layout, toasts, forms, formatters, Chart.js defaults) and its own page script.
  Pages live in `frontend/pages/`; `BASE` handles relative paths. Use HTML `pattern` syntax valid under the
  regex `v` flag (escape `-` only inside character classes).

## Gotchas

- `init_db.py` splits SQL files on `;` at end of line and on `/` lines for PL/SQL blocks; keep that style.
- Seed passwords and test users are documented in `database/03_data.sql` and README; tests depend on that data.
- The Oracle container runs with `TZ=America/Bogota` so `SYSDATE` matches local dates.

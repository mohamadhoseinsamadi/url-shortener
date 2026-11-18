# URL Shortener

A URL shortening REST API built with **FastAPI** and **PostgreSQL**, developed as a team midterm project. Supports creating short links, redirection, listing, deletion, and a bonus **TTL (expiration)** feature.

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/links` | Create a short link |
| GET | `/{code}` | Redirect to the original URL |
| GET | `/links` | List all shortened links |
| DELETE | `/links/{code}` | Delete a short link |
| POST | `/admin/cleanup` | Remove expired links (TTL cleanup) |

Validation errors are returned as `400` with a standardized JSON body (`status`, `message`, `data`). Interactive docs are available at `/docs`.

## Tech Stack

- Python 3.12, FastAPI, Uvicorn
- SQLAlchemy + Alembic (migrations)
- PostgreSQL (psycopg2)
- Poetry for dependency management

## Setup & Run

```bash
poetry install
cp .env.example .env        # set DB_PASSWORD and connection details
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

The API is served at http://127.0.0.1:8000.

## TTL (Expiration)

- `LINK_TTL_SECONDS` in `.env` controls link lifetime.
- Expiry is checked on redirect (`app/services/service.py → get_original_url()`).
- Expired links are removed by `POST /admin/cleanup` (`cleanup_expired_links()`), designed to be triggered by an external scheduler (e.g. a cron job).

## Project Structure

```
app/
  controller/   # API routes
  services/     # Business logic (short code generation, TTL)
  repository/   # Data access
  model/        # SQLAlchemy models
  schemas/      # Pydantic schemas
  database/     # Engine and session setup
alembic/        # Database migrations
docs/           # Course submission checklist and Postman screenshots
```

## Course Documentation

The original midterm submission checklist (test coverage, TTL details, Postman screenshots) is kept in [docs/course-checklist.md](docs/course-checklist.md).
# AI-Assisted SDLC with Codex

A practical, project-based tutorial for building an AI-assisted software development lifecycle with OpenAI Codex.

The repository grows with the tutorial. The application is a small Work Item API used to introduce increasingly realistic software-engineering problems and progressively greater Codex autonomy.

## Chapter 1 baseline

At this point the repository is intentionally conventional. Codex can help write code, but the repository does not yet contain durable agent instructions, standardized verification commands, reusable agent workflows, or autonomous issue-to-PR automation. Those capabilities will be added only when the project creates a reason for them.

The sample application currently supports basic CRUD operations for work items.

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- pytest
- Ruff
- mypy
- Docker Compose
- GitHub Actions

## Run with Docker

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`. FastAPI's interactive API documentation is available at `http://localhost:8000/docs`.

Try the health endpoint:

```bash
curl http://localhost:8000/health
```

## Run locally

Create a virtual environment and install the project:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Start PostgreSQL:

```bash
docker compose up -d db
```

Apply the database migration and start the API:

```bash
alembic upgrade head
uvicorn work_item_api.main:app --reload
```

Run the current checks individually:

```bash
pytest
ruff check .
mypy src
```

Notice that there is not yet a single project verification command. That gap is intentional and becomes part of the tutorial.

## Repository evolution

Each major tutorial milestone will be tagged so readers can compare the repository before and after a new SDLC capability is introduced.

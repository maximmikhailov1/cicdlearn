# cicdlearn

Learning project for CI/CD with GitHub Actions. Monorepo: FastAPI backend, Next.js frontend, Nginx, PostgreSQL, MongoDB.

## Stack

- **Backend**: Python 3.12, FastAPI, asyncpg, Motor (MongoDB)
- **Frontend**: Next.js 15, React 19, TypeScript
- **Infra**: Nginx (reverse proxy), Docker Compose
- **Databases**: PostgreSQL 16, MongoDB 7

## Prerequisites

- Docker and Docker Compose (API version 3)
- For local development without Docker: Node.js 18+, Python 3.12+, running PostgreSQL and MongoDB

## Run locally

From the repo root:

```bash
docker compose up --build
```

- App: http://localhost (Nginx → frontend and `/api/` → backend)
- Backend only: http://localhost:8000
- PostgreSQL: localhost:5432 (user `app`, password `app`, db `app`)
- MongoDB: localhost:27017

## Tests

### Backend (pytest)

Backend tests need PostgreSQL and MongoDB. Easiest: run tests inside the backend container:

```bash
docker compose up -d postgres mongo
docker compose run --rm backend pytest
```

From the host (with Postgres and Mongo reachable at `localhost`):

```bash
cd backend
export APP_POSTGRES_URL="postgresql+asyncpg://app:app@localhost:5432/app"
export APP_MONGO_URL="mongodb://localhost:27017"
pip install -r requirements.txt
pytest
```

### Frontend (Jest)

```bash
cd frontend
npm install
npm test
```

## CI/CD

Workflows are not included by default. See [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) for a step-by-step guide to configuring GitHub Actions yourself.

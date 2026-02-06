# CI/CD with GitHub Actions: Learning Guide

This guide explains how to configure CI/CD for the cicdlearn project. It does **not** provide ready-made workflow files: you write the YAML yourself and learn from mistakes. Use this document as a mentor: it tells you what to do, what to avoid, and how to debug.

---

## 1. Introduction

**CI (Continuous Integration)** means automatically running tests, linters, and builds on every push or pull request. **CD (Continuous Delivery/Deployment)** adds automatic deployment (e.g. to a server or a cloud platform).

In this repo you will automate:

- Running backend tests (pytest) and frontend tests (Jest)
- Optionally: linting (e.g. Ruff, ESLint), formatting checks
- Optionally: building Docker images and pushing them to a registry
- Optionally: deploying (e.g. to a VPS or Railway/Render/Fly.io)

**Why GitHub Actions?** It is built into GitHub, has a generous free tier, and is widely used. Learning it transfers to other CI systems (GitLab CI, Jenkins, etc.).

---

## 2. Preparing the Repository

### Branches

- Use a main branch (`main` or `master`) and feature branches.
- You can enable branch protection (Settings → Branches): require status checks to pass before merging. That way broken CI blocks merge.

### Secrets and Variables

- **Settings → Secrets and variables → Actions**
- **Secrets**: for sensitive data (API keys, SSH keys, registry passwords). Never commit these.
- **Variables**: for non-sensitive configuration (e.g. registry URL, environment name).

You will need secrets later if you:

- Push Docker images (e.g. `GITHUB_TOKEN` for GHCR, or Docker Hub username/password)
- Deploy via SSH (host, user, private key) or a provider token (Railway, Render, etc.)

---

## 3. First Workflow: Tests

Goal: on every push and pull request, run backend and frontend tests.

### Where to put the workflow

- Directory: `.github/workflows/`
- File name: any `*.yml` or `*.yaml` (e.g. `tests.yml` or `ci.yml`)

### Triggers

Example: run on push and pull_request to `main` (and optionally other branches):

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

You can omit `branches` to run on all branches.

### Jobs and steps

- A **job** is a sequence of **steps** that run in the same runner (VM).
- Each step can run a script or use a pre-defined **action** (e.g. `actions/checkout@v4`).

**Task:** Create a workflow that:

1. Checks out the repo (`actions/checkout@v4`).
2. Runs backend tests: set up Python 3.12, install dependencies from `backend/requirements.txt`, run `pytest` in the `backend/` directory.  
   Hint: use `actions/setup-python@v5` with `python-version` and a path to the backend. You need PostgreSQL and MongoDB for the app; in CI you can use **service containers** (Postgres and Mongo) so the backend job can connect to them.
3. Runs frontend tests: set up Node.js (e.g. 20), install dependencies in `frontend/`, run `npm test`.  
   Hint: `actions/setup-node@v4` and `working-directory: frontend`.

You can put backend and frontend in **one job** (sequential steps) or in **two jobs** (parallel). Two jobs give clearer logs and allow parallel execution.

### Typical mistakes

- **Wrong `working-directory`**: if you run `pytest` or `npm test` from the repo root without `working-directory`, they may not find config or code. Set `working-directory: backend` or `frontend` on the relevant steps.
- **No service containers for backend**: the app expects Postgres and Mongo. In the job that runs pytest, add a `services:` block with `postgres` and `mongo`, and set env vars (e.g. `APP_POSTGRES_URL`, `APP_MONGO_URL`) so the app connects to `localhost` and the ports exposed by the services.
- **Different Python/Node versions**: use the same versions as in the project (e.g. Python 3.12, Node 20) so CI matches local and Docker.
- **Slow runs**: install dependencies every time. Later you can add caching (e.g. `actions/cache` for pip and npm) to speed up runs.

---

## 4. Linters and Formatting

After tests pass, you can add steps to run:

- **Backend**: Ruff (or Black + isort). Example: `pip install ruff` then `ruff check backend/` and optionally `ruff format --check backend/`.
- **Frontend**: ESLint (and optionally Prettier). Example: in `frontend/` run `npm run lint` (and a format check if you have one).

Decide whether the workflow should **fail** when lint or format fails. Failing is strict and keeps the main branch clean; not failing means you only see warnings.

---

## 5. Building Docker Images

Goal: build backend and frontend images and optionally push them to a registry.

### Building in CI

- Use a job that has Docker available (the default `ubuntu-latest` runner has Docker).
- Build from the repo root so Docker context can see `backend/` or `frontend/`:
  - `docker build -t backend ./backend`
  - `docker build -t frontend ./frontend`

You can build in the same job as tests or in a separate job (e.g. only on push to `main`).

### Pushing to a registry

**GitHub Container Registry (ghcr.io):**

- Log in with `docker/login-action` using the built-in `GITHUB_TOKEN` (or a PAT with `write:packages`).
- Tag the image: `ghcr.io/<your-username>/cicdlearn-backend:latest` (or use `github.sha` for a unique tag).
- Push with `docker push`.

**Docker Hub:**

- Store `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (or password) in repo secrets.
- Use `docker/login-action` and then tag and push.

### Typical mistakes

- Forgetting **docker login** before push (push will fail with auth error).
- Wrong **build context**: e.g. `docker build -t backend .` from repo root but Dockerfile expects files under `backend/`; the Dockerfile path and context must match.
- Not **tagging** the image before push (the registry needs a full name and tag).

---

## 6. Deploy (Overview)

Deployment is not implemented for you; here is what you would do when you are ready.

- **VPS**: use a job that runs on push to `main`, SSHs into the server, pulls (or builds) images and runs `docker compose up -d`. Store host, user, and SSH key in secrets.
- **PaaS** (Railway, Render, Fly.io): use the provider’s GitHub integration or CLI in a job, with a token in secrets.

Important:

- Never commit secrets; use Actions secrets or variables.
- Prefer deploying only from a protected branch (e.g. `main`) and only after tests (and optionally build) succeed.

---

## 7. Typical Errors and How to Find Them

- **Tests fail in CI but pass locally**: Check Python/Node versions, env vars (e.g. `APP_POSTGRES_URL`), and that Postgres/Mongo are actually running in the job (service containers).
- **“Module not found” or “command not found”**: Check `working-directory` and that install steps ran in the same job and directory.
- **Docker build fails**: Check Dockerfile path, build context, and that all required files are in the context (e.g. no `.dockerignore` excluding needed files).
- **Push to registry fails**: Check login step and image tag (correct registry host and name).

Use the **Actions** tab: open the run, open the failing job, and read the step logs. The error message usually points to the cause.

---

## 8. Checklist and Next Steps

Suggested order:

1. **Tests**: workflow that runs pytest and npm test (with Postgres + Mongo for backend).
2. **Linters**: add Ruff and ESLint (and optionally format checks).
3. **Build**: add a job that builds backend and frontend Docker images.
4. **Push images**: add login and push to GHCR or Docker Hub.
5. **Deploy** (optional): add a deploy job when you have a target environment.

Ideas to go further:

- **Matrix**: run tests on several Python or Node versions.
- **Caching**: cache pip and npm dependencies to speed up runs.
- **Artifacts**: upload test results or coverage (e.g. `actions/upload-artifact`).
- **Notifications**: on failure, send a message to Telegram or Slack (e.g. with a webhook).

---

When you hit a wall, re-read the relevant section and the GitHub Actions docs; then fix one step at a time. Errors are part of the learning process.

# FLOOD_AID

## 1. Introduction

Flood Aid is the system designed to support charitable donations for victims affected by natural disasters (e.g., Typhoon Yagi in the North) with the goal of ensuring transparency, openness, and efficiency in managing donations and fund distribution.

## 2. Stack & Framework

- [Django](https://www.djangoproject.com/) - Batteries-included Python web framework.
- [PostgreSQL](https://www.postgresql.org/) - Well-know open source database system.

## 3. Dev tools (must install for local development)

- [Pyenv](https://github.com/pyenv/pyenv): Python version management.
- [Docker](https://www.docker.com/products/docker-desktop/): Docker app for launching services like db, redis, etc

## 4. Getting started

### Environment & dependencies setup (Pyenv installed)

- Create virtual env for easier maintain:

```bash
python -m venv .venv
```

- Sourcing the .venv:

```bash
source .venv/bin/activate
```

- Install package manager:

```bash
pip install -r requirements-init.txt
```

- Install all dependencies:

```bash
poetry install
```

```bash
pip install psycopg2-binary
```

### Run backend

- Edit the environment variables in [.env](.env) file.
- Start docker:

```bash
docker compose up -d
```

- Run migrations

```bash
bin/manage.sh makemigrations
bin/manage.sh migrate
```

- Start server

```bash
bin/manage.sh runserver 8000
```

## 5. Utilities

### Useful command

- `bin/manage.sh runserver 8000`: Run local server.
- `bin/manage.sh createsuperuser`: Create superuser to access to admin at
  [http://localhost:8000/admin/](http://localhost:8000/admin/)
- `bin/manage.sh shell_plus`: Interactive shell_plus to access db, query, e.t.c.

### Packages management

- [Poetry](https://python-poetry.org/docs/): the package dependencies management we use.
- When you want to add a dependency just run `poetry add your_package_name`.

### Fixtures

- Populate disaster areas:

```bash
bin/manage.sh populate_disaster_areas
```

- Populate campaigns:

```bash
bin/manage.sh populate_campaigns
```

### Code conventions

- For code convention we are using:
  - [Ruff](https://pypi.org/project/ruff/): for speedy combination code formatting with flake8, blake or isort, e.t.c.
- The above tool have been wrapped with the executable script [bin/lint.sh](bin/lint.sh):
  - To lint only, run: `bin/lint.sh`
  - To automatically format, run: `bin/lint.sh --fix`

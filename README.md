## Calendly Like APIs
The docs are available at `/docs` once the application is running


## Local Development

### Setup just
MacOS:
```shell
brew install just
```

Debian/Ubuntu:
```shell
apt install just
````

Others: [link](https://github.com/casey/just?tab=readme-ov-file#packages)

### Setup poetry
```shell
pip install poetry
```

Other ways: [link](https://python-poetry.org/docs/#installation)

### Setup Postgres (16.3)
```shell
just up
```
### Copy the environment file and install dependencies
1. `cp .env.example .env`
2. `poetry install`

### Run the uvicorn server
With default settings:
```shell
just run
```
With extra configs (e.g. logging file)
```shell
just run --log-config logging.ini
```

### Linters
Format the code with `ruff --fix` and `ruff format`
```shell
just lint
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
just mm *migration_name*
```
- Run migrations
```shell
just migrate
```
- Downgrade migrations
```shell
just downgrade downgrade -1  # or -2 or base or hash of the migration
```
## Calendly Like APIs
This project is an API implmentation to support some of the features provided by a calendar blocking app.

The API docs are available at `/docs` once the application is running

Support for
- Availablity templates for event creators
- Support for multiple events
- Overlap for available spots between two users
- Timezone support
- Email invites after blocking the calendar

### Some notes of architecture
This project mostly follows [clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) except gateway implmentation for email service. This is done for a faster local testing, but should be updated later on.

Dependency injection is done manually throughout the project. It would be a nice addition to setup some auto-wiring with [lagom](https://lagom-di.readthedocs.io/en/latest/) in future.

Doesn't have yet:
- Request level idempotency support
- different DB isolation levels on demand per session  


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
import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import app_configs, settings
from src.schedule.routes.v1 import availability, event, schedule
from src.user.routes.v1 import user

app = FastAPI(**app_configs)
app.include_router(user.router)
app.include_router(availability.router)
app.include_router(event.router)
app.include_router(schedule.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

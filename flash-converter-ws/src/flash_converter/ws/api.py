import contextlib
import logging

import kombu.exceptions
from fastapi import FastAPI
from flash_converter_wf.server import celery_app
from starlette.middleware.cors import ALL_METHODS, CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from flash_converter.ws.config import settings
from flash_converter.ws.router import router as task_router


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    settings.display_settings(logging.getLogger("uvicorn.error"))
    yield


app = FastAPI(lifespan=lifespan)

# Configuration of the CORS middleware
_ALLOW_HEADERS = (
    "Accept",
    "Accept-Language",
    "Authorization",
    "Content-Language",
    "Content-Type",
    "Origin",
    "X-Requested-With",
)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=ALL_METHODS,
    allow_headers=_ALLOW_HEADERS,
)

app.include_router(task_router, prefix="/tasks")


# add an exception handler to intercept ConnectionRefusedError exceptions
# and respond a 503 HTTP status code with a message
@app.exception_handler(kombu.exceptions.OperationalError)
async def connection_refused_error_handler(_: Request, exc: kombu.exceptions.OperationalError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"message": f"Service unavailable: {exc}"},
    )


@app.get("/health/celery")
async def health_celery() -> dict[str, str]:
    """
    Check if the Celery system is operational (workers connectivity, etc.).
    """
    try:
        celery_app.control.ping()
    except kombu.exceptions.OperationalError as exc:
        return {"status": "error", "message": str(exc)}
    else:
        return {"status": "ok", "message": "Celery is running"}


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "message": "Webservice is running"}

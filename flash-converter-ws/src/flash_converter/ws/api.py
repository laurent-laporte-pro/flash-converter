import kombu.exceptions
from fastapi import FastAPI
from flash_converter_wf.server import celery_app
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from flash_converter.ws.config import settings
from flash_converter.ws.router import router as task_router

app = FastAPI()

# Configuration du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins.split(","),
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"),
    allow_headers=(
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
    ),
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

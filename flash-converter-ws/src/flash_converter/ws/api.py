import kombu.exceptions
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from flash_converter.tasks import celery_app
from flash_converter.ws.router import router as task_router

app = FastAPI()

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

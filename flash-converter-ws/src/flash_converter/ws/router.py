"""
Define the routes to manage tasks.
"""

import typing as t
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from starlette.responses import StreamingResponse

from flash_converter.ws.config import settings
from flash_converter.ws.schema import Task
from flash_converter.tasks import Payload, convert_video

if t.TYPE_CHECKING:
    from celery.result import AsyncResult

router = APIRouter(tags=["tasks"])


@router.post("/", response_model=Task, status_code=201)
async def create_task(video: UploadFile) -> Task:
    """
    Create a new task to convert a video file to MP3.
    """

    suffix = Path(video.filename).suffix
    file_location = Path(settings.UPLOAD_DIR) / f"{uuid.uuid4()}{suffix}"

    # Store the file on disk
    work_dir = file_location.parent
    work_dir.mkdir(parents=True, exist_ok=True)
    with file_location.open("wb") as buffer:
        buffer.write(await video.read())

    # Convert the video in background
    output_path = file_location.with_suffix(".mp3")
    job = convert_video.delay(video.filename, str(file_location), str(output_path))
    return Task.from_job(job)


@router.get("/{task_id}/status")
async def get_task_status(task_id: str) -> Task:
    """
    Get the status of a task.
    """

    job: AsyncResult = convert_video.AsyncResult(task_id)
    return Task.from_job(job)


async def stream_file(file_path: Path, size=8192) -> t.AsyncGenerator[bytes, None]:
    with file_path.open("rb") as buffer:
        while chunk := buffer.read(size):
            yield chunk


@router.get("/{task_id}/result")
async def get_task_result(task_id: str) -> StreamingResponse:
    """
    Get the result of a task.
    """
    job: AsyncResult = convert_video.AsyncResult(task_id)
    if job.state != "SUCCESS":
        raise HTTPException(status_code=404, detail=f"Task not completed yet: {job.state}")

    payload = Payload(*job.get())
    mp3_name = Path(payload.filename).with_suffix(".mp3").name

    return StreamingResponse(
        content=stream_file(Path(payload.audio_path)),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"attachment; filename={mp3_name}"},
    )


@router.delete("/{task_id}", status_code=204)
async def revoke_task(task_id: str) -> None:
    """
    Revoke a task.
    """
    job: AsyncResult = convert_video.AsyncResult(task_id)

    payload = Payload(*job.get())
    Path(payload.video_path).unlink(missing_ok=True)
    Path(payload.audio_path).unlink(missing_ok=True)

    # Empêche l'exécution d'une tâche en ajoutant son ID à une liste noire (revoked tasks).
    # Cela n'efface pas la tâche de Redis, sauf si elle est configurée pour expirer.
    job.revoke(terminate=True)

    # Supprime uniquement le résultat de la tâche (si le backend de résultats est utilisé),
    # mais n'affecte pas les métadonnées dans le broker.
    job.forget()

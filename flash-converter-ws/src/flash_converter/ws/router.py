"""
Define the routes to manage tasks.
"""

import tempfile
import typing as t
from pathlib import Path

from fastapi import APIRouter, UploadFile
from flash_converter_wf import launcher
from flash_converter_wf.video.video_model import VideoModel
from starlette.responses import StreamingResponse

from flash_converter.ws.config import settings

router = APIRouter(tags=["tasks"])


@router.post("/", status_code=201)
async def create_task(video: UploadFile) -> launcher.TaskId:
    """
    Create a new task to convert a video file to MP3.
    """
    workdir = Path(tempfile.mkdtemp(dir=settings.UPLOAD_DIR, prefix="ws-"))
    file_location = workdir / video.filename
    with file_location.open("wb") as buffer:
        buffer.write(await video.read())
    video_model = VideoModel(workdir=workdir, video_name=video.filename)
    return launcher.submit_task(video_model)


@router.get("/{task_id}/status")
async def get_task_status(task_id: launcher.TaskId) -> str:
    """
    Get the status of a task.
    """
    return launcher.get_task_status(task_id)


async def stream_file(file_path: Path, size=8192) -> t.AsyncGenerator[bytes, None]:
    with file_path.open("rb") as buffer:
        while chunk := buffer.read(size):
            yield chunk


@router.get("/{task_id}/result")
async def get_task_result(task_id: launcher.TaskId, timeout: int = launcher.CONVERSION_TIMEOUT) -> StreamingResponse:
    """
    Get the result of a task.
    """
    video_model = launcher.get_task_result(task_id, timeout=timeout)
    return StreamingResponse(
        content=stream_file(video_model.output_path),
        media_type="video/mp4",
        headers={"Content-Disposition": f"attachment; filename={video_model.video_name}"},
    )


@router.delete("/{task_id}", status_code=204)
async def revoke_task(task_id: launcher.TaskId, timeout: int = launcher.REVOKE_TIMEOUT) -> None:
    """
    Revoke a task.
    """
    launcher.revoke_task(task_id, timeout=timeout)

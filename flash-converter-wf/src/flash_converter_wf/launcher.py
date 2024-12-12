"""
Launch a new video processing in the workflow.
"""

import shutil
import tempfile
from pathlib import Path

from celery import chain
from celery.result import AsyncResult

from flash_converter_wf.config import settings
from flash_converter_wf.video.convert_to_audio import convert_to_audio_task
from flash_converter_wf.video.detect_voice import detect_voice_task
from flash_converter_wf.video.embed_subtitles import embed_subtitles_task
from flash_converter_wf.video.extract_audio_track import extract_audio_track_task
from flash_converter_wf.video.preflight_check import preflight_check_task
from flash_converter_wf.video.process_subtitles import process_subtitles_task
from flash_converter_wf.video.video_model import VideoModel


def upload_video(video_path: Path) -> VideoModel:
    """
    Upload a video file to the workflow.

    Args:
        video_path: User-provided path to the video file to process.

    Returns:
        VideoAttrs object with the working directory and video name.
    """
    # Prepare tha working directory
    workdir = Path(tempfile.mkdtemp(dir=settings.UPLOAD_DIR, prefix="video-"))
    # Copy the video file
    shutil.copy(video_path, workdir / video_path.name)
    # Prepare the video attributes
    return VideoModel(workdir=workdir, video_name=video_path.name)


def submit_task(video: VideoModel) -> str:
    """
    Submit a new video processing task to the workflow.

    Args:
        video: VideoModel object with the working directory and video name.

    Returns:
        UUID of the task.
    """
    # Definition of the Celery workflow:
    # - PreflightCheck: Check if video is valid -- raise `InvalidVideoError` if not.
    # - DetectVoice: Detect voice in video: find start and end timecodes of each voice segment.
    # - ConvertToAudio: Convert video to audio segments (one per voice): prepare subtitles extraction.
    # - ProcessSubtitles: Extract subtitles from audio segments: this process is done in parallel in the `subtitle` swimlane.
    # - EmbedSubtitles: Embed subtitles in video.
    video_chain = chain(
        preflight_check_task.s(),
        extract_audio_track_task.s(),
        detect_voice_task.s(),
        convert_to_audio_task.s(),
        process_subtitles_task.s(),
        embed_subtitles_task.s(),
    )
    task: AsyncResult = video_chain(video.model_dump(mode="json"))
    return task.task_id


def get_task_status(task_id: str) -> str:
    """
    Get the status of a video conversion task.

    Args:
        task_id: UUID of the task to check.

    Returns:
        Status of the task.
    """
    task: AsyncResult = AsyncResult(task_id)
    return task.state


def get_task_result(task_id: str, timeout: int = 10) -> Path:
    """
    Get the result of a video conversion task.

    Args:
        task_id: UUID of the task to check.
        timeout: Timeout in seconds to wait for the task to complete.

    Returns:
        Path to the video file with embedded subtitles.
    """
    result: AsyncResult = AsyncResult(task_id)
    video = VideoModel(**result.get(timeout=timeout))
    return video.output_path


def revoke_task(task_id: str, timeout: int = 1) -> None:
    """
    Revoke a video conversion task.

    Args:
        task_id: UUID of the task to revoke.
        timeout: Timeout in seconds to wait for the task to revoke.
    """
    result: AsyncResult = AsyncResult(task_id)
    result.revoke(terminate=True, wait=True, timeout=timeout)

    if result.status in {"FAILURE", "REVOKED"}:
        # In case of failure or revocation, we can't get the result
        # and cleanup the working directory
        return

    # Use a short timeout to avoid blocking the application,
    # and cleanup the working directory
    video = VideoModel(**result.get(timeout=timeout))
    shutil.rmtree(video.workdir, ignore_errors=True)

    result.forget()


def convert_video(video_path: Path, timeout: int = 10) -> Path:
    """
    Launch a new video processing in the workflow.

    Args:
        video_path: Path to the video file to process (e.g. '/path/to/video.mp4').
        timeout: Timeout in seconds to wait for the task to complete.

    Returns:
        Path to the video file with embedded subtitles.
    """
    video: VideoModel = upload_video(video_path)
    task_id: str = submit_task(video)
    return get_task_result(task_id, timeout=timeout)

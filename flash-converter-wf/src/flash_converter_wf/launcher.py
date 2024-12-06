"""
Launch a new video processing in the workflow.
"""

import shutil
import tempfile
from pathlib import Path

from celery import chain

from flash_converter_wf.config import settings
from flash_converter_wf.video.convert_to_audio import convert_to_audio_task
from flash_converter_wf.video.detect_voice import detect_voice_task
from flash_converter_wf.video.embed_subtitles import embed_subtitles_task
from flash_converter_wf.video.preflight_check import preflight_check_task
from flash_converter_wf.video.process_subtitles import process_subtitles_task
from flash_converter_wf.video.video_attrs import VideoAttrs


def launch_workflow(video_path: Path) -> Path:
    """
    Launch a new video processing in the workflow.

    Args:
        video_path: Path to the video file to process (e.g. '/path/to/video.mp4').

    Returns:
        Path to the video file with embedded subtitles.
    """
    # Prepare tha working directory
    workdir = Path(tempfile.mkdtemp(dir=settings.UPLOAD_DIR, prefix="video-"))
    task_id = workdir.name

    # Copy the video file
    shutil.copy(video_path, workdir / video_path.name)

    # Prepare the video attributes
    video_attrs = VideoAttrs(
        task_id=task_id,
        workdir=workdir,
        video_name=video_path.name,
    )

    # Definition of the Celery workflow:
    # - PreflightCheck: Check if video is valid -- raise `InvalidVideoError` if not.
    # - DetectVoice: Detect voice in video: find start and end timecodes of each voice segment.
    # - ConvertToAudio: Convert video to audio segments (one per voice): prepare subtitles extraction.
    # - ProcessSubtitles: Extract subtitles from audio segments: this process is done in parallel in the `subtitle` swimlane.
    # - EmbedSubtitles: Embed subtitles in video.

    video_chain = chain(
        preflight_check_task.s(),
        detect_voice_task.s(),
        convert_to_audio_task.s(),
        process_subtitles_task.s(),
        embed_subtitles_task.s(),
    )
    task = video_chain(video_attrs.to_json())

    # Run the task and wait for the result
    result = task.get(timeout=10)

    video_attrs = VideoAttrs(**result)
    return video_attrs.output_path

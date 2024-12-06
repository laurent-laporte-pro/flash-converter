"""
Use the following command to start the Celery worker::

    celery -A flash_converter_wf.server.celery_app worker --loglevel=info
"""

from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.convert_to_subtitles import convert_to_subtitles_task
from flash_converter_wf.video.convert_to_audio import convert_to_audio_task
from flash_converter_wf.video.detect_voice import detect_voice_task
from flash_converter_wf.video.embed_subtitles import embed_subtitles_task
from flash_converter_wf.video.preflight_check import preflight_check_task
from flash_converter_wf.video.process_subtitles import process_subtitles_task

__all__ = [
    "celery_app",
    "preflight_check_task",
    "convert_to_audio_task",
    "detect_voice_task",
    "process_subtitles_task",
    "embed_subtitles_task",
    "convert_to_subtitles_task",
]

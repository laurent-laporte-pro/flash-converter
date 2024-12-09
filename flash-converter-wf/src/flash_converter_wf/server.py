"""
Use the following command to start the Celery worker::

    celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q default,voice,audio,subtitle

Instead of managing all queues with a single worker, you can use multiple commands to start the workers::

    celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q default -n default@%h
    celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q voice -n voice@%h
    celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q audio -n audio@%h
    celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q subtitle -n subtitle@%h

This will start four workers, each listening on a different queue.

NOTE:

    The ``-n`` option is used to set the hostname of the worker.
    This is required when you have multiple workers running on the same machine.

    If the workers are launched in separate pods or images (for example, with Docker or Kubernetes),
    each worker instance will have its own isolated environment, including its own hostname.
    In this case, it is not necessary to specify a different hostname for each worker.
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

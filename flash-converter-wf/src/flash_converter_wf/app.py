from celery import Celery

from flash_converter_wf.config import settings

celery_app = Celery(
    "flash_converter_wf.app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.broker_connection_retry_on_startup = settings.BROKER_CONNECTION_RETRY_ON_STARTUP

# The "default" queue is used for tasks which are not CPU-bound.
DEFAULT_QUEUE = "default"

# The "voice" queue is used for voice detection and use 'silero_vad' model with pytorch.
VOICE_DETECTION_QUEUE = "voice"

# The "audio" queue is used for audio conversion and use 'pydub' library to convert to mp3 format.
AUDIO_CONVERSION_QUEUE = "audio"

# The "subtitle" queue is used for subtitle extraction and use 'whisper' model.
SUBTITLE_EXTRACTION_QUEUE = "subtitle"

celery_app.conf.task_default_queue = DEFAULT_QUEUE
celery_app.conf.task_routes = {
    "flash_converter_wf.video.preflight_check.preflight_check_task": {"queue": DEFAULT_QUEUE},
    "flash_converter_wf.video.detect_voice.detect_voice_task": {"queue": VOICE_DETECTION_QUEUE},
    "flash_converter_wf.video.convert_to_audio.convert_to_audio_task": {"queue": AUDIO_CONVERSION_QUEUE},
    "flash_converter_wf.video.process_subtitles.process_subtitles_task": {"queue": DEFAULT_QUEUE},
    "flash_converter_wf.subtitle.convert_to_subtitles.convert_to_subtitles_task": {"queue": SUBTITLE_EXTRACTION_QUEUE},
    "flash_converter_wf.video.embed_subtitles.embed_subtitles_task": {"queue": DEFAULT_QUEUE},
}

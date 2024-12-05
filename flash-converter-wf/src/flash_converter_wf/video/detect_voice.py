from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_attrs import VideoAttrs


@celery_app.task()
def detect_voice_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- DetectVoice

    Detect voice in video: find start and end timecodes of each voice segment.
    """
    video_attrs = VideoAttrs.from_json(obj)
    # code
    return video_attrs.to_json()

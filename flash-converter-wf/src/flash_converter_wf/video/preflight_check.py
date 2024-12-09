from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


@celery_app.task()
def preflight_check_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- PreflightCheck

    Check if video is valid -- raise `InvalidVideoError` if not.
    """
    video_attrs = VideoModel.from_json(obj)
    # code
    return video_attrs.to_json()

from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


@celery_app.task()
def preflight_check_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- PreflightCheck

    Check if video is valid -- raise `InvalidVideoError` if not.
    """
    video = VideoModel(**obj)  # type: ignore
    # code
    return video.to_json()

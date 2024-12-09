from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


@celery_app.task()
def embed_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- EmbedSubtitles

    Embed subtitles in video.
    """
    video = VideoModel(**obj)  # type: ignore
    # code
    return video.to_json()

from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_attrs import VideoAttrs


@celery_app.task()
def embed_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- EmbedSubtitles

    Embed subtitles in video.
    """
    video_attrs = VideoAttrs.from_json(obj)
    # code
    return video_attrs.to_json()

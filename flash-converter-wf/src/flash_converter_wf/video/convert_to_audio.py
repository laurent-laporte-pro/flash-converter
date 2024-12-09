from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


@celery_app.task()
def convert_to_audio_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- ConvertToAudio

    Convert video to audio segments (one per voice): prepare subtitles extraction.
    """
    video_attrs = VideoModel.from_json(obj)
    # code
    return video_attrs.to_json()

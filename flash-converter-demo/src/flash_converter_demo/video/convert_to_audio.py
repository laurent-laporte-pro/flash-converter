import celery

from .video_attrs import VideoAttrs


class ConvertToAudioTask(celery.Task):
    """
    Step: video -- ConvertToAudio

    Convert video to audio segments (one per voice): prepare subtitles extraction.
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

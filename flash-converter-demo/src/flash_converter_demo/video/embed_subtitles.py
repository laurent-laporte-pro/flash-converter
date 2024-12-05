import celery

from .video_attrs import VideoAttrs


class EmbedSubtitlesTask(celery.Task):
    """
    Step: video -- EmbedSubtitles

    Embed subtitles in video.
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

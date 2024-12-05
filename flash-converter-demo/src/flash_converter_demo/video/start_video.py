import celery

from .video_attrs import VideoAttrs


class StartVideoTask(celery.Task):
    """
    Step: video -- StartVideo

    Start video conversion (entry point).
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

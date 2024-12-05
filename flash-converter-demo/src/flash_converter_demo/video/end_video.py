import celery

from .video_attrs import VideoAttrs


class EndVideoTask(celery.Task):
    """
    Step: video -- EndVideo

    End video conversion (exit point).
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

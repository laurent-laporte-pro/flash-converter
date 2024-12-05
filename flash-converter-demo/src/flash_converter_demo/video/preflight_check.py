import celery

from .video_attrs import VideoAttrs


class PreflightCheckTask(celery.Task):
    """
    Step: video -- PreflightCheck

    Check if video is valid -- raise `InvalidVideoError` if not.
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

import celery

from .video_attrs import VideoAttrs


class ProcessSubtitlesTask(celery.Task):
    """
    Step: video -- ProcessSubtitles

    Extract subtitles from audio segments: this process is done in parallel in the `subtitle` swimlane.
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

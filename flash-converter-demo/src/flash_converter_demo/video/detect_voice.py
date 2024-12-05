import celery

from .video_attrs import VideoAttrs


class DetectVoiceTask(celery.Task):
    """
    Step: video -- DetectVoice

    Detect voice in video: find start and end timecodes of each voice segment.
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        video_attrs = VideoAttrs.from_json(obj)
        # code
        return video_attrs.to_json()

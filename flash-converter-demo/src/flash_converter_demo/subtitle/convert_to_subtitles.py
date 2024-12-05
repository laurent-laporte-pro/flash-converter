import celery

from .subtitle_attrs import SubtitleAttrs


class ConvertToSubtitlesTask(celery.Task):
    """
    Step: subtitle -- ConvertToSubtitles

    Convert audio to subtitles using AI.
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        subtitle_attrs = SubtitleAttrs.from_json(obj)
        # code
        return subtitle_attrs.to_json()

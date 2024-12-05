import celery

from .subtitle_attrs import SubtitleAttrs


class EndSubtitlesTask(celery.Task):
    """
    Step: subtitle -- EndSubtitles

    End subtitles extraction (exit point).
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        subtitle_attrs = SubtitleAttrs.from_json(obj)
        # code
        return subtitle_attrs.to_json()

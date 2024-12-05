import celery

from .subtitle_attrs import SubtitleAttrs


class StartSubtitlesTask(celery.Task):
    """
    Step: subtitle -- StartSubtitles

    Start subtitles extraction (entry point).
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        subtitle_attrs = SubtitleAttrs.from_json(obj)
        # code
        return subtitle_attrs.to_json()

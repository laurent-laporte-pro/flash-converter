from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.subtitle_attrs import SubtitleAttrs


@celery_app.task()
def convert_to_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: subtitle -- ConvertToSubtitles

    Convert audio to subtitles using AI.
    """
    subtitle_attrs = SubtitleAttrs.from_json(obj)

    filename = f"subtitles_{subtitle_attrs.segment_start}_{subtitle_attrs.segment_end}.srt"

    # Create subtitles file
    with (subtitle_attrs.workdir / filename).open(mode="w") as f:
        print("1", file=f)
        print(f"{subtitle_attrs.segment_start} --> {subtitle_attrs.segment_end}", file=f)
        print("Hello, world!", file=f)

    return subtitle_attrs.to_json()

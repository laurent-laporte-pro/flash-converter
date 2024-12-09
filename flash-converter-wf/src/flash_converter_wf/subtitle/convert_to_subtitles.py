from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.subtitle_model import SubtitleModel


@celery_app.task()
def convert_to_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: subtitle -- ConvertToSubtitles

    Convert audio to subtitles using AI.
    """
    subtitle = SubtitleModel(**obj)  # type: ignore
    filename = f"subtitles_{subtitle.segment_start}_{subtitle.segment_end}.srt"

    # Create subtitles file
    with (subtitle.workdir / filename).open(mode="w") as f:
        print("1", file=f)
        print(f"{subtitle.segment_start} --> {subtitle.segment_end}", file=f)
        print("Hello, world!", file=f)

    return subtitle.to_json()

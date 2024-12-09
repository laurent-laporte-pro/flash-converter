from celery import group

from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.convert_to_subtitles import convert_to_subtitles_task
from flash_converter_wf.subtitle.subtitle_model import SubtitleModel
from flash_converter_wf.video.video_model import VideoModel


@celery_app.task()
def process_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- ProcessSubtitles

    Extract subtitles from audio segments: this process is done in parallel in the `subtitle` swimlane.
    """
    video_attrs = VideoModel.from_json(obj)

    segments = [
        "00:00:10.000,00:00:20.000",
        "00:00:30.000,00:00:35.000",
        "00:01:27.000,00:01:30.000",
    ]
    with (video_attrs.workdir / "subtitles.txt").open(mode="w") as f:
        for segment in segments:
            print(segment, file=f)

    # prepare the subtitle attributes
    subtitle_attrs = [
        SubtitleModel(
            workdir=video_attrs.workdir,
            segment_start=segment.split(",")[0],
            segment_end=segment.split(",")[1],
        )
        for segment in segments
    ]

    # Process the subtitles in parallel in the `subtitle` swimlane
    subtitle_tasks = [convert_to_subtitles_task.s(subtitle.to_json()) for subtitle in subtitle_attrs]
    subtitle_group = group(subtitle_tasks)
    subtitle_group()

    return video_attrs.to_json()

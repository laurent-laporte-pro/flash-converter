import csv
import time
import typing as t

from celery import group
from celery.result import GroupResult

from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.convert_to_subtitles import convert_to_subtitles_task
from flash_converter_wf.subtitle.subtitle_model import SegmentModel, SubtitleModel
from flash_converter_wf.video.video_model import VideoModel


@celery_app.task()
def process_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- ProcessSubtitles

    Extract subtitles from audio segments: this process is done in parallel in the `subtitle` swimlane.
    """
    video = VideoModel(**obj)  # type: ignore

    # Read the voice segments from the CSV file
    with video.voice_segments_path.open(mode="r") as f:
        segments = [SegmentModel(**row) for row in csv.DictReader(f)]  # type: ignore

    # prepare the subtitle attributes
    subtitle_attrs = [SubtitleModel(workdir=video.workdir, segment=segment) for segment in segments]

    # Process the subtitles in parallel in the `subtitle` swimlane
    subtitle_tasks = [convert_to_subtitles_task.s(subtitle.model_dump(mode="json")) for subtitle in subtitle_attrs]
    subtitle_group = group(subtitle_tasks)
    subtitle_group()

    # This loop is not very efficient, but it's a simple way to wait for all tasks to complete
    result: GroupResult = t.cast(GroupResult, subtitle_group.apply_async())
    while not result.ready():  # type: ignore
        time.sleep(0.1)

    return video.model_dump(mode="json")

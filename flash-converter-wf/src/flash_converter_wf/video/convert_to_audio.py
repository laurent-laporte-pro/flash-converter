import csv
import typing as t
from pathlib import Path

from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.subtitle_model import SegmentModel, SubtitleModel
from flash_converter_wf.video.video_model import VideoModel


def _load_audio_file(audio_path: Path) -> t.Any:
    from pydub import AudioSegment

    return AudioSegment.from_file(audio_path, format="wav")


@celery_app.task()
def convert_to_audio_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- ConvertToAudio

    Convert video to audio segments (one per voice): prepare subtitles extraction.
    """
    video = VideoModel(**obj)  # type: ignore

    # Charger l'audio avec pydub pour extraction
    audio = _load_audio_file(video.audio_path)

    # Read the voice segments from the CSV file
    with video.voice_segments_path.open(mode="r") as f:
        for row in csv.DictReader(f):
            segment = SegmentModel(**row)  # type: ignore
            subtitle = SubtitleModel(workdir=video.workdir, segment=segment)
            start_ms = max(0, int(segment.start_time.total_seconds() * 1000))
            end_ms = min(len(audio), int(segment.end_time.total_seconds() * 1000))
            audio_segment = audio[start_ms:end_ms]
            audio_segment.export(subtitle.audio_path, format="mp3")

    return video.model_dump(mode="json")

import csv
import datetime
import re
import typing as t
from pathlib import Path

from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


def _load_audio_file(audio_path: Path) -> t.Any:
    from pydub import AudioSegment

    return AudioSegment.from_file(audio_path, format="wav")


def _parse_timedelta(video_time: str) -> datetime.timedelta:
    mo = re.fullmatch(r"(\d+):(\d+):(\d+)\.(\d+)", video_time)
    if mo is None:
        msg = f"Invalid video time format: '{video_time}'"
        raise ValueError(msg)
    hours, minutes, seconds, milliseconds = map(int, mo.groups())
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


@celery_app.task()
def convert_to_audio_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- ConvertToAudio

    Convert video to audio segments (one per voice): prepare subtitles extraction.
    """
    video = VideoModel(**obj)  # type: ignore

    # Charger l'audio avec pydub pour extraction
    audio = _load_audio_file(video.audio_path)

    with video.voice_segments_path.open(mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = row["index"]
            start_time = _parse_timedelta(row["start_time"])
            end_time = _parse_timedelta(row["end_time"])
            start_ms = max(0, int((start_time.total_seconds() - 0.5) * 1000))
            end_ms = min(len(audio), int((end_time.total_seconds() + 0.5) * 1000))
            segment = audio[start_ms:end_ms]
            segment.export(video.workdir / f"segment_{index}.mp3", format="mp3")

    return video.to_json()

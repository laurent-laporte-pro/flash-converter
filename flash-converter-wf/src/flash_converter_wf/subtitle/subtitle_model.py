import datetime
from pathlib import Path

from pydantic import BaseModel


class SegmentModel(BaseModel):
    """
    Task attributes for Segment swimlane.
    """

    index: int
    start_time: datetime.timedelta
    end_time: datetime.timedelta


class SubtitleModel(BaseModel):
    """
    Task attributes for Subtitle swimlane.
    """

    workdir: Path
    segment: SegmentModel

    @property
    def audio_path(self) -> Path:
        return self.workdir / f"segment_{self.segment.index:05d}.mp3"

    @property
    def subtitles_path(self) -> Path:
        return self.workdir / f"segment_{self.segment.index:05d}.srt"

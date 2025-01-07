import datetime
from pathlib import Path

from pydantic import BaseModel


class VideoModel(BaseModel):
    """
    Task attributes for Video swimlane.

    - workdir: Working directory for the task.
    - video_name: Name of the video file to process.
    """

    workdir: Path
    video_name: str

    # voice segmentation parameters
    sampling_rate: int = 16000
    threshold: float = 0.6
    before: datetime.timedelta = datetime.timedelta(seconds=0.5)  # seconds
    after: datetime.timedelta = datetime.timedelta(seconds=0.5)  # seconds

    @property
    def input_path(self):
        return self.workdir / self.video_name

    @property
    def output_path(self):
        return self.workdir / f"output_{self.video_name}"

    @property
    def audio_path(self):
        return self.workdir / "audio.wav"

    @property
    def voice_segments_path(self):
        return self.workdir / "voice_segments.csv"

    @property
    def subtitles_path(self) -> Path:
        return self.workdir / "subtitles.srt"

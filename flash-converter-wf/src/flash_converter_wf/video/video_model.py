import json
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

    def to_json(self) -> dict[str, str]:
        return json.loads(self.model_dump_json())

import dataclasses
from pathlib import Path


@dataclasses.dataclass
class VideoModel:
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

    def __post_init__(self):
        self.workdir = Path(self.workdir)

    @classmethod
    def from_json(cls, attrs: dict[str, str]) -> "VideoModel":
        return cls(
            workdir=Path(attrs["workdir"]),
            video_name=attrs["video_name"],
        )

    def to_json(self) -> dict[str, str]:
        return {
            "workdir": str(self.workdir),
            "video_name": self.video_name,
        }

import dataclasses
from pathlib import Path


@dataclasses.dataclass
class VideoAttrs:
    """
    Task attributes for Video swimlane.

    - task_id: Task identifier.
    - workdir: Working directory for the task.
    - task_name: Task name.
    """

    task_id: str
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
    def from_json(cls, attrs: dict[str, str]) -> "VideoAttrs":
        return cls(
            task_id=attrs["task_id"],
            workdir=Path(attrs["workdir"]),
            video_name=attrs["video_name"],
        )

    def to_json(self) -> dict[str, str]:
        return {
            "task_id": self.task_id,
            "workdir": str(self.workdir),
            "video_name": self.video_name,
        }

import dataclasses
from pathlib import Path


@dataclasses.dataclass
class SubtitleAttrs:
    """
    Task attributes for Subtitle swimlane.
    """

    task_id: str
    workdir: Path
    segment_start: str
    segment_end: str

    def __post_init__(self):
        self.workdir = Path(self.workdir)

    @classmethod
    def from_json(cls, attrs: dict[str, str]) -> "SubtitleAttrs":
        return cls(
            task_id=attrs["task_id"],
            workdir=Path(attrs["workdir"]),
            segment_start=attrs["segment_start"],
            segment_end=attrs["segment_end"],
        )

    def to_json(self) -> dict[str, str]:
        return {
            "task_id": self.task_id,
            "workdir": str(self.workdir),
            "segment_start": self.segment_start,
            "segment_end": self.segment_end,
        }

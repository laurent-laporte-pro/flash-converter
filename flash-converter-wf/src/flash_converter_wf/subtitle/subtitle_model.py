import dataclasses
from pathlib import Path


@dataclasses.dataclass
class SubtitleModel:
    """
    Task attributes for Subtitle swimlane.
    """

    workdir: Path
    segment_start: str
    segment_end: str

    def __post_init__(self):
        self.workdir = Path(self.workdir)

    @classmethod
    def from_json(cls, attrs: dict[str, str]) -> "SubtitleModel":
        return cls(
            workdir=Path(attrs["workdir"]),
            segment_start=attrs["segment_start"],
            segment_end=attrs["segment_end"],
        )

    def to_json(self) -> dict[str, str]:
        return {
            "workdir": str(self.workdir),
            "segment_start": self.segment_start,
            "segment_end": self.segment_end,
        }

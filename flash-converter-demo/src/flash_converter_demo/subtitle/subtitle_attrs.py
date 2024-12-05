import dataclasses
from pathlib import Path


@dataclasses.dataclass
class SubtitleAttrs:
    """
    Task attributes for Subtitle swimlane.
    """
    
    task_id: str
    task_name: str
    workdir: Path
    
    def __post_init__(self):
        self.workdir = Path(self.workdir)
    
    @classmethod
    def from_json(cls, attrs: dict[str, str]) -> "SubtitleAttrs":
        return cls(
            task_id=attrs["task_id"],
            task_name=attrs["task_name"],
            workdir=Path(attrs["workdir"]),
        )
    
    def to_json(self) -> dict[str, str]:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "workdir": str(self.workdir),
        }

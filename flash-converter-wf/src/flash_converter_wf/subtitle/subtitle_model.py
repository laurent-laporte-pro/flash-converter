import json
from pathlib import Path

from pydantic import BaseModel


class SubtitleModel(BaseModel):
    """
    Task attributes for Subtitle swimlane.
    """

    workdir: Path
    segment_start: str
    segment_end: str

    def to_json(self) -> dict[str, str]:
        return json.loads(self.model_dump_json())

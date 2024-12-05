import csv
from pathlib import Path

SRC_DIR = Path(__file__).parent
CSV_PATH = SRC_DIR / "workflow.csv"


def camel_to_snake(name: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')


def create_python_pkg(pkg_dir: Path) -> None:
    pkg_dir.mkdir(exist_ok=True)
    pkg_dir.joinpath("__init__.py").touch()


ATTRS_TEMPLATE = '''\
import dataclasses
from pathlib import Path


@dataclasses.dataclass
class {Swimlane}Attrs:
    """
    Task attributes for {Swimlane} swimlane.
    """
    
    task_id: str
    task_name: str
    workdir: Path
    
    def __post_init__(self):
        self.workdir = Path(self.workdir)
    
    @classmethod
    def from_json(cls, attrs: dict[str, str]) -> "{Swimlane}Attrs":
        return cls(
            task_id=attrs["task_id"],
            task_name=attrs["task_name"],
            workdir=Path(attrs["workdir"]),
        )
    
    def to_json(self) -> dict[str, str]:
        return {{
            "task_id": self.task_id,
            "task_name": self.task_name,
            "workdir": str(self.workdir),
        }}
'''


def generate_swimlane_attrs(swimlane_dir: Path, swimlane: str) -> None:
    swimlane_path = (swimlane_dir / f"{swimlane}_attrs.py")
    if not swimlane_path.exists():
        with swimlane_path.open(mode="w") as f:
            f.write(ATTRS_TEMPLATE.format(
                Swimlane=swimlane.title(),
            ))


TASK_TEMPLATE = '''\
import celery

from .{swimlane}_attrs import {Swimlane}Attrs


class {name}Task(celery.Task):
    """
    Step: {swimlane} -- {name}

    {description}
    """

    def run(self, obj: dict[str, str]) -> dict[str, str]:
        {swimlane}_attrs = {Swimlane}Attrs.from_json(obj)
        # code
        return {swimlane}_attrs.to_json()
'''


def generate_workflow(csv_path: Path, src_dir: Path) -> None:
    with csv_path.open(mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            swimlane: str = row["swimlane"]
            name: str = row["name"]
            description: str = row["description"]

            swimlane_dir = src_dir / camel_to_snake(swimlane)
            create_python_pkg(swimlane_dir)
            generate_swimlane_attrs(swimlane_dir, swimlane)

            module_name = (swimlane_dir / camel_to_snake(name)).with_suffix(".py")
            with module_name.open(mode="w") as f:
                f.write(TASK_TEMPLATE.format(
                    swimlane=swimlane,
                    Swimlane=swimlane.title(),
                    name=name,
                    description=description,
                ))


if __name__ == '__main__':
    generate_workflow(CSV_PATH, SRC_DIR)

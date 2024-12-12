import datetime
from pathlib import Path

from flash_converter_wf.subtitle.subtitle_model import SegmentModel, SubtitleModel


class TestSegmentModel:
    def test_from_json(self) -> None:
        data = {"index": "00008", "start_time": "PT1M2.345S", "end_time": "PT2M10.789S"}
        segment = SegmentModel(**data)  # type: ignore
        assert segment.index == 8
        assert segment.start_time == datetime.timedelta(hours=0, minutes=1, seconds=2, milliseconds=345)
        assert segment.end_time == datetime.timedelta(hours=0, minutes=2, seconds=10, milliseconds=789)

    def test_to_json(self) -> None:
        segment = SegmentModel(
            index=8,
            start_time=datetime.timedelta(hours=0, minutes=1, seconds=2, milliseconds=345),
            end_time=datetime.timedelta(hours=0, minutes=2, seconds=10, milliseconds=789),
        )
        data = segment.model_dump(mode="json")
        assert data == {"index": 8, "start_time": "PT1M2.345S", "end_time": "PT2M10.789S"}


class TestSubtitleModel:
    def test_from_json(self) -> None:
        data = {
            "workdir": "/tmp",
            "segment": {"index": "00008", "start_time": "PT1M2.345S", "end_time": "PT2M10.789S"},
        }
        subtitle = SubtitleModel(**data)  # type: ignore
        assert subtitle.workdir == Path("/tmp")
        assert subtitle.segment.index == 8
        assert subtitle.segment.start_time == datetime.timedelta(hours=0, minutes=1, seconds=2, milliseconds=345)
        assert subtitle.segment.end_time == datetime.timedelta(hours=0, minutes=2, seconds=10, milliseconds=789)

    def test_to_json(self) -> None:
        segment = SegmentModel(
            index=8,
            start_time=datetime.timedelta(hours=0, minutes=1, seconds=2, milliseconds=345),
            end_time=datetime.timedelta(hours=0, minutes=2, seconds=10, milliseconds=789),
        )
        subtitle = SubtitleModel(workdir=Path("/tmp"), segment=segment)
        data = subtitle.model_dump(mode="json")
        assert data == {
            "workdir": "/tmp",
            "segment": {"index": 8, "start_time": "PT1M2.345S", "end_time": "PT2M10.789S"},
        }

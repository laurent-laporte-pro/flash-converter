import csv
import re
from pathlib import Path

from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.subtitle_model import SegmentModel, SubtitleModel
from flash_converter_wf.video.video_model import VideoModel


def _concatenate_srt(voice_segments_path: Path, subtitles_path: Path, workdir: Path) -> None:
    """
    Concatenate the srt files.

    Args:
        voice_segments_path: Source file with voice segments.
        subtitles_path: Destination file with subtitles.
        workdir: Working directory containing the srt files.
    """
    general_index = 1
    with open(subtitles_path, mode="w") as subtitles, voice_segments_path.open(mode="r") as f:
        for row in csv.DictReader(f):
            segment = SegmentModel(**row)  # type: ignore
            subtitle = SubtitleModel(workdir=workdir, segment=segment)
            with subtitle.subtitles_path.open(mode="r") as fs:
                for line in fs:
                    if re.fullmatch(r"\d+", line.rstrip()):
                        subtitles.write(f"{general_index}\n")
                        general_index += 1
                    else:
                        subtitles.write(line)


def _embed_subtitles(src_path: Path, dst_path: Path, subtitles_path: Path) -> None:
    """
    Embed subtitles in video.

    Args:
        src_path: Path to the source video file.
        dst_path: Path to the destination video file with subtitles.
        subtitles_path: Path to the subtitles file.
    """
    import ffmpeg

    (
        ffmpeg.input(filename=str(src_path))
        .output(filename=str(dst_path), vf=f"subtitles={subtitles_path}")
        .run(overwrite_output=True)
    )


@celery_app.task()
def embed_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- EmbedSubtitles

    Embed subtitles in video.
    """
    video = VideoModel(**obj)  # type: ignore

    _concatenate_srt(video.voice_segments_path, video.subtitles_path, video.workdir)
    _embed_subtitles(video.input_path, video.output_path, video.subtitles_path)

    # code
    return video.model_dump(mode="json")

import typing as t
from pathlib import Path

from flash_converter.tasks.app import celery_app


class Payload(t.NamedTuple):
    filename: str  # Display name of the file
    video_path: str  # Internal path to the video file
    audio_path: str  # Internal path to the audio file


@celery_app.task
def convert_video(filename: str, video_path: Path, output_path: Path) -> Payload:
    """
    Convert a video file to MP3

    :param filename: The original filename
    :param video_path: The path to the video file to convert
    :param output_path: The path to the output MP3 file
    """

    # The Python library `ffmpeg-python` is a wrapper around the FFmpeg command line tool.
    # To use it, you need to have FFmpeg installed on your system.
    # On macOS, you can install FFmpeg using Homebrew: `brew install ffmpeg`

    import ffmpeg

    ffmpeg.input(str(video_path)).output(filename=str(output_path), acodec="libmp3lame").run()

    return Payload(filename=filename, video_path=str(video_path), audio_path=str(output_path))

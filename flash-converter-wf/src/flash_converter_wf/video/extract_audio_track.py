from pathlib import Path

from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


def _extract_audio_track(video_path: Path, audio_path: Path, *, sampling_rate: int = 16000) -> None:
    # The Python library `typed-ffmpeg` (or `ffmpeg-python`) is a wrapper around the FFmpeg command line tool.
    # To use it, you need to have FFmpeg installed on your system.
    # On macOS, you can install FFmpeg using Homebrew: `brew install ffmpeg`
    import ffmpeg

    ffmpeg.input(str(video_path)).output(
        filename=str(audio_path),
        acodec="pcm_s16le",
        ac=1,
        ar=sampling_rate,
    ).run()


@celery_app.task()
def extract_audio_track_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- Extract Audio Track

    Extract audio track from video file.
    """
    video = VideoModel(**obj)  # type: ignore
    sampling_rate = 16000
    _extract_audio_track(video.input_path, video.audio_path, sampling_rate=sampling_rate)
    return video.to_json()

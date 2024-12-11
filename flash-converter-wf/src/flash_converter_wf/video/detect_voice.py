import datetime
from pathlib import Path

from flash_converter_wf.app import celery_app
from flash_converter_wf.video.video_model import VideoModel


def _get_voice_segments(audio_path: Path, *, sampling_rate: int = 16000, threshold: float = 0.6):
    # Load the "Silero VAD" model
    import torch

    torch.set_num_threads(1)
    model, utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad")
    # get_speech_timestamps, sauve_audio, read_audio, VADIterator, collect_chunks = utils
    get_speech_timestamps, _, read_audio, _, _ = utils
    # Read the audio file and detect speech segments
    wav = read_audio(audio_path, sampling_rate=sampling_rate)
    return get_speech_timestamps(wav, model, sampling_rate=sampling_rate, threshold=threshold)


def _format_timedelta(timedelta: datetime.timedelta) -> str:
    hours, remainder = divmod(timedelta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timedelta.microseconds // 1000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"


@celery_app.task()
def detect_voice_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- DetectVoice

    Detect voice in audio track: find start and end timecodes of each voice segment.
    """
    video = VideoModel(**obj)  # type: ignore

    sampling_rate = 16000
    voice_segments = _get_voice_segments(video.audio_path, sampling_rate=sampling_rate, threshold=0.6)

    with video.voice_segments_path.open(mode="w") as f:
        print("index,start_time,end_time", file=f)
        for index, segment in enumerate(voice_segments, 1):
            start_time = datetime.timedelta(seconds=segment["start"] / sampling_rate)
            end_time = datetime.timedelta(seconds=segment["end"] / sampling_rate)
            print(f"{index:05d},{_format_timedelta(start_time)},{_format_timedelta(end_time)}", file=f)

    return video.to_json()

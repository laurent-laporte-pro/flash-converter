import csv
import datetime
from pathlib import Path

from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.subtitle_model import SegmentModel
from flash_converter_wf.video.video_model import VideoModel


class LazySileroVADModel:
    """
    Functional object to load the "Silero VAD" model lazily.
    """

    def __init__(self):
        self._model = None
        self._utils = None

    def __call__(self):
        if self._model is None:
            import torch

            torch.set_num_threads(1)
            self._model, self._utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad")

        return self._model, self._utils


get_silero_vad_model = LazySileroVADModel()


def _get_voice_segments(audio_path: Path, *, sampling_rate: int = 16000, threshold: float = 0.6):
    # Load the "Silero VAD" model
    model, utils = get_silero_vad_model()
    # get_speech_timestamps, sauve_audio, read_audio, VADIterator, collect_chunks = utils
    get_speech_timestamps, _, read_audio, _, _ = utils
    # Read the audio file and detect speech segments
    wav = read_audio(audio_path, sampling_rate=sampling_rate)
    return get_speech_timestamps(wav, model, sampling_rate=sampling_rate, threshold=threshold)


@celery_app.task()
def detect_voice_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- DetectVoice

    Detect voice in audio track: find start and end timecodes of each voice segment.
    """
    video = VideoModel(**obj)  # type: ignore

    voice_segments = _get_voice_segments(video.audio_path, sampling_rate=video.sampling_rate, threshold=video.threshold)

    with video.voice_segments_path.open(mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "start_time", "end_time"])
        writer.writeheader()
        for index, voice_segment in enumerate(voice_segments, 1):
            start_time = datetime.timedelta(seconds=voice_segment["start"] / video.sampling_rate) - video.before
            start_time = max(datetime.timedelta(), start_time)
            end_time = datetime.timedelta(seconds=voice_segment["end"] / video.sampling_rate) + video.after
            segment = SegmentModel(index=index, start_time=start_time, end_time=end_time)
            writer.writerow(segment.model_dump(mode="json"))

    return video.model_dump(mode="json")

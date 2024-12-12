from flash_converter_wf.app import celery_app
from flash_converter_wf.subtitle.subtitle_model import SubtitleModel


class LazyWhisperModel:
    """
    Functional object to load the "whisper" model lazily.
    """

    def __init__(self):
        self._whisper_model = None

    def __call__(self):
        if self._whisper_model is None:
            import whisper

            self._whisper_model = whisper.load_model("base")  # or "large"

        return self._whisper_model


get_whisper_model = LazyWhisperModel()


def format_time(seconds: int) -> str:
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


@celery_app.task()
def convert_to_subtitles_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: subtitle -- ConvertToSubtitles

    Convert audio to subtitles using AI.
    """
    subtitle = SubtitleModel(**obj)  # type: ignore

    whisper_model = get_whisper_model()
    result = whisper_model.transcribe(str(subtitle.audio_path), task="transcribe", language="fr")

    with open(subtitle.subtitles_path, mode="w", encoding="utf-8") as f:
        for srt_index, srt_segment in enumerate(result["segments"]):
            start = srt_segment["start"]
            end = srt_segment["end"]
            text = srt_segment["text"]

            real_index = subtitle.segment.index + srt_index
            real_start = subtitle.segment.start_time.total_seconds() + start
            real_end = subtitle.segment.start_time.total_seconds() + end

            f.write(f"{real_index}\n")
            f.write(f"{format_time(real_start)} --> {format_time(real_end)}\n")
            f.write(f"{text}\n\n")

    return subtitle.model_dump(mode="json")

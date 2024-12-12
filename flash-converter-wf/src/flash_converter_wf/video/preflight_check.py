import mimetypes

from flash_converter_wf.app import celery_app
from flash_converter_wf.video.exceptions import InvalidVideoError
from flash_converter_wf.video.video_model import VideoModel

mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/x-matroska", ".mkv")
mimetypes.add_type("video/quicktime", ".mov")
mimetypes.add_type("video/x-msvideo", ".avi")
mimetypes.add_type("video/x-ms-wmv", ".wmv")
mimetypes.add_type("video/x-flv", ".flv")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/x-m4v", ".m4v")
mimetypes.add_type("video/3gpp", ".3gp")
mimetypes.add_type("video/3gpp2", ".3g2")
mimetypes.add_type("video/mpeg", ".mpg")
mimetypes.add_type("video/mpeg", ".mpeg")
mimetypes.add_type("video/ogg", ".ogv")
mimetypes.add_type("video/mp2t", ".ts")


@celery_app.task()
def preflight_check_task(obj: dict[str, str]) -> dict[str, str]:
    """
    Step: video -- PreflightCheck: Check the video file format.

    Args:
        obj: Dictionary containing video information.

    Returns:
        JSON representation of the video model.

    Raises:
        InvalidVideoError: If the video format is not supported.
    """
    video = VideoModel(**obj)  # type: ignore
    mime_type = mimetypes.guess_type(video.input_path)[0]
    if mime_type is None:
        msg = f"Unrecognized file format: '{video.input_path.name}'"
        raise InvalidVideoError(msg)
    if not mime_type.startswith("video/"):
        msg = f"Invalid file format: '{mime_type}', expected a video file."
        raise InvalidVideoError(msg)
    return video.model_dump(mode="json")

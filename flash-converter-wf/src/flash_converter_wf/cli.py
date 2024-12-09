from pathlib import Path

import celery.exceptions
import click

from flash_converter_wf.__about__ import __app_name__, __version__
from flash_converter_wf.launcher import (
    convert_video,
    get_task_result,
    get_task_status,
    revoke_task,
    submit_task,
    upload_video,
)

VERSION = f"{__app_name__} {__version__}"


@click.group(context_settings={"max_content_width": 120})
@click.version_option(version=VERSION)
def click_app() -> None:
    """
    Convert a video file to add subtitles to it quickly and efficiently.

    Use the `convert` command to convert a video file synchronously, or
    the `submit`, `status`, `result`, and `revoke` commands to manage
    video conversion tasks asynchronously.
    """


@click_app.command(name="convert")
@click.argument("video_path", type=click.Path(exists=True, dir_okay=False))
@click.option("-t", "--timeout", type=int, default=10, help="Timeout in seconds to wait for the task to complete.")
@click.option("-o", "--output", type=click.Path(dir_okay=False), help="Output path for the converted video.")
def convert_cmd(video_path: str, timeout: int, output: str) -> None:
    """
    Convert a video file to add subtitles to it.

    This command submits a video conversion task to the Celery workflow
    and waits for the task to complete to display the result.

    \b
    VIDEO_PATH: Path to the video file to process (e.g. '/path/to/video.mp4').
    """
    click.echo(f"Converting video '{video_path}'...")
    try:
        result_path = convert_video(Path(video_path), timeout=timeout)
    except celery.exceptions.TimeoutError as exc:
        msg = f"Task timed out: {exc}"
        raise SystemExit(msg) from None
    else:
        if output:
            result_path.rename(output)
            result_path = Path(output)
        click.echo(f"Result: {result_path}")


@click_app.command(name="submit")
@click.argument("video_path", type=click.Path(exists=True, dir_okay=False))
def submit_cmd(video_path: str) -> None:
    """
    Submit a video conversion task to the Celery workflow and display the task ID.

    \b
    VIDEO_PATH: Path to the video file to process (e.g. '/path/to/video.mp4').
    """
    click.echo(f"Submitting video '{video_path}'...")
    video = upload_video(Path(video_path))
    task_id: str = submit_task(video)
    click.echo(f"Task ID: {task_id}")


@click_app.command(name="status")
@click.argument("task_id")
def status_cmd(task_id: str) -> None:
    """
    Get the status of a video conversion task.

    \b
    TASK_ID: UUID of the task to check.
    """
    click.echo(f"Checking task status: {task_id}...")
    status = get_task_status(task_id)
    click.echo(f"Task status: {status}")


@click_app.command(name="result")
@click.argument("task_id")
@click.option("-t", "--timeout", type=int, default=10, help="Timeout in seconds to wait for the task to complete.")
@click.option("-o", "--output", type=click.Path(dir_okay=False), help="Output path for the converted video.")
def result_cmd(task_id: str, timeout: int, output: str) -> None:
    """
    Get the result of a video conversion task.

    \b
    TASK_ID: UUID of the task to check.
    """
    click.echo(f"Getting task result: {task_id}...")
    try:
        result_path = get_task_result(task_id, timeout=timeout)
    except celery.exceptions.TimeoutError as exc:
        msg = f"Task timed out: {exc}"
        raise SystemExit(msg) from None
    else:
        if output:
            result_path.rename(output)
            result_path = Path(output)
        click.echo(f"Result: {result_path}")


@click_app.command(name="revoke")
@click.argument("task_id")
@click.option("-t", "--timeout", type=int, default=1, help="Timeout in seconds to wait for the task to revoke.")
def revoke_cmd(task_id: str, timeout: int) -> None:
    """
    Revoke a video conversion task.

    \b
    TASK_ID: UUID of the task to revoke.
    """
    click.echo(f"Revoking task: {task_id}...")
    try:
        revoke_task(task_id, timeout=timeout)
    except celery.exceptions.TimeoutError as exc:
        msg = f"Revoke timed out: {exc}"
        raise SystemExit(msg) from None
    else:
        click.echo("Task revoked successfully.")

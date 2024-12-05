from pathlib import Path

import click

from flash_converter_wf.__about__ import __app_name__, __version__
from flash_converter_wf.launcher import launch_workflow

VERSION = f"{__app_name__} {__version__}"


@click.command()
@click.version_option(version=VERSION)
@click.argument("video_path", type=click.Path(exists=True, dir_okay=False))
def click_app(video_path: str):
    """
    Convert video to audio with embedded subtitles.

    \b
    VIDEO_PATH: Path to the video file to process (e.g. '/path/to/video.mp4').
    """
    click.echo(f"Converting video: {video_path}")
    result_path = launch_workflow(Path(video_path))
    click.echo(f"Result: {result_path}")

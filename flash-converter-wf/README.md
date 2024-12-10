# Flash Converter Workflow

Convert video files to add subtitles to them quickly and efficiently.

[![PyPI - Version](https://img.shields.io/pypi/v/flash-converter-wf.svg)](https://pypi.org/project/flash-converter-wf)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flash-converter-wf.svg)](https://pypi.org/project/flash-converter-wf)

-----

## Table of Contents

- [Project Description](#project-description)
    - [Description of the workflow](#description-of-the-workflow)
- [Using the Celery Application](#using-the-celery-application)
    - [Start a single Celery worker](#start-a-single-celery-worker)
    - [Start multiple Celery workers](#start-multiple-celery-workers)
- [Using the Command Line Interface (CLI)](#using-the-command-line-interface-cli)
    - [Getting help](#getting-help)
    - [Synchronous conversion](#synchronous-conversion)
    - [Asynchronous conversion](#asynchronous-conversion)
- [Using as a Python library](#using-as-a-python-library)
- [License](#license)

## Project Description

This project is a demonstration of the implementation of a workflow using [Celery][celery] as an
asynchronous task manager, [RabbitMQ][rabbitmq] as a message broker and [Redis][redis] as a Celery backend.

The Python project serves several purposes:

- **Provide a Celery application:**
  The same Celery application can be started on multiple processes to listen on different queues:
  "default", "voice", "audio" and "subtitle".

- **Provide a Command Line Interface (CLI):**
  The "flash-converter-wf" CLI can be used to submit conversion tasks to the Celery workflow.
  This CLI is useful for testing the workflow.

- **Provide a Python library:**
  The "flash-converter-wf" library can be used in a FastAPI application.
  The FastAPI application allows you to submit conversion tasks to the Celery workflow,
  and retrieve the converted files.

[celery]: http://www.celeryproject.org/

[rabbitmq]: https://www.rabbitmq.com/

[redis]: https://redis.io/

### Description of the workflow

The "video" processing workflow consists of several steps that are executed in sequence:

1. **PreflightCheck**: Check the video file format: `InvalidVideoError` is raised if the video format is not supported.
2. **DetectVoice**: find voice segments in the video file.
3. **ConvertToAudio**: extract the audio track of each segment.
4. **ProcessSubtitles**: delegate the processing of subtitles to the "subtitle" workflow for parallel processing.
    - **ConvertToSubtitles**: convert the audio track to text.
5. **EmbedSubtitles**: embed the subtitles in the video file.

The workflow is represented by the following diagram:

![Flash Converter BPM Model](docs/img/flash-converter-BPM.svg)

## Using the Celery Application

Starting the Celery application can be done in two different ways depending on whether you
want to start a single Celery worker or multiple Celery workers.

Starting a single Celery worker is useful for testing the workflow, while starting multiple
Celery workers is useful for running the workflow in a production environment.

### Start a single Celery worker

The Celery application can be started using the following command:

```shell
celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q default,voice,audio,subtitle
```

### Start multiple Celery workers

The project is configured to allow starting several Celery workers listening on different queues:
"default", "voice", "audio" et "subtitle".

To start multiple Celery workers, use the following commands (one command in a separate terminal):

```shell
celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q default -n default@%h
celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q voice -n voice@%h
celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q audio -n audio@%h
celery -A flash_converter_wf.server.celery_app worker --loglevel=info -Q subtitle -n subtitle@%h
```

This will start four workers, each listening on a different queue.

The ``-n`` option is used to set the hostname of the worker.
This is required when you have multiple workers running on the same machine.

If the workers are launched in separate pods or images (for example, with Docker or Kubernetes),
each worker instance will have its own isolated environment, including its own hostname.
In this case, it is not necessary to specify a different hostname for each worker.

## Using the Command Line Interface (CLI)

The "flash-converter-wf" CLI can be used to submit conversion tasks to the Celery workflow.

### Getting help

☞ To display the help message, use the following command:

```shell
python -m flash_converter_wf --help
```

### Synchronous conversion

☞ To convert a video file synchronously, use the following command:

```shell
python -m flash_converter_wf convert path/to/IMG_3903.mov
```

The command will convert the video file and display the path of the converted file.

### Asynchronous conversion

☞ To submit a conversion task, use the following command:

```shell
python -m flash_converter_wf submit path/to/IMG_3903.mov
```

The command will submit a conversion task to the Celery workflow and display the task ID.

☞ To display the status of a task, use the following command:

```shell
python -m flash_converter_wf status 0cd16305-ae90-423c-b8db-fbaa65af1305
```

The command will display the status of the task with the specified task ID: "PENDING", "SUCCESS" or "FAILURE".

☞ To retrieve the result of a task, use the following command:

```shell
python -m flash_converter_wf result 0cd16305-ae90-423c-b8db-fbaa65af1305
```

The command will display the path of the converted file if the task was successful.

☞ To revoke a task and clean up the working directory, use the following command:

```shell
python -m flash_converter_wf revoke 0cd16305-ae90-423c-b8db-fbaa65af1305
```

## Using as a Python library

The "flash-converter-wf" library can be used in a FastAPI application.

```shell
pip install flash-converter-wf
```

In FastAPI routers, you can use the following functions from the `flash_converter_wf.launcher.upload_video` module:

```python
from pathlib import Path

from flash_converter_wf.video.video_model import VideoModel


def upload_video(video_path: Path) -> VideoModel:
    """Upload a video file to the workflow."""
    ...


def submit_task(video: VideoModel) -> str:
    """Submit a new video processing task to the workflow."""
    ...


def get_task_status(task_id: str) -> str:
    """Get the status of a video processing task."""
    ...


def get_task_result(task_id: str, timeout: int = 10) -> Path:
    """Get the result of a video processing task."""
    ...


def revoke_task(task_id: str, timeout: int = 1) -> None:
    """Revoke a video processing task."""
    ...
```

## License

`flash-converter-wf` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

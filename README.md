<img alt="Flash Converter Logo" src="docs/img/flash-converter-icon.png" style="float: right; width: 20em; height: 20em;"/>

# Flash Converter

## Description of the project

The purpose of this converter is to automatically embed subtitles in the video.
It uses IA models to detect the voices in the video and convert them into text.
The text is then used to generate subtitles that are embedded in the video.

This is a demonstration project that uses
- FastAPI to implement a web service that converts video using a Celery pipeline.
- Celery and RabbitMQ to implement a workflow for video conversion tasks.
- FFmpeg to process the video files.
- Pydub to convert audio to MP3.
- Torch and TorchAudio to detect voices in the video.
- OpenAI-Whisper to convert voices to text.

This project is composed of the following subprojects:

- **flash-converter-ws**: FastAPI web service that launches the video conversion tasks.
- **flash-converter-wf**: Celery workflow that processes the video conversion tasks.

Each subproject is a standalone project that can be run independently.

## Development

### Prerequisites

- Python 3.12
- Docker
- Docker Compose
- FFmpeg binaries
- a Redis server (a Docker container is provided)
- a RabbitMQ server (a Docker container is provided)

### Running the project

Open the `[docker-compose.yaml](docker-compose.yaml)` file and set the environment variables for the services.

```bash
docker-compose up
```

### End-to-end testing

The HTTP Request file [end-to-end.http](tests/end-to-end.http) is available in the `tests` directory.
It demonstrates the conversion of a video file to an MP3 file.

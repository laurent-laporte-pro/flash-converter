<img alt="Flash Converter Logo" src="docs/img/flash-converter-icon.png" style="float: right; width: 20em; height: 20em;"/>

# Flash Converter

## Description of the project

This is a demonstration project for converting Video to MP3 using Python FastAPI, FFmpeg, and Celery with
a RabbitMQ message broker.

This project is composed of the following subprojects:

- **flash-converter-ws**: FastAPI web service that converts video to MP3.
- **flash-converter-tasks**: Celery worker that processes the video conversion tasks.
- **flash-converter-demo**: a demo of some advanced features of Video/Audio processing using AI models.

Each subproject is a standalone project that can be run independently.

## Development

### Prerequisites

- Python 3.8
- Docker
- Docker Compose
- FFmpeg
- Redis
- RabbitMQ

### Running the project

Open the `[docker-compose.yaml](docker-compose.yaml)` file and set the environment variables for the services.

```bash
docker-compose up
```

### End-to-end testing

The HTTP Request file [end-to-end.http](tests/end-to-end.http) is available in the `tests` directory.
It demonstrates the conversion of a video file to an MP3 file.

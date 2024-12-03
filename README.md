# Flash Converter

## Description of the project

This is a demonstration project for converting Video to MP3 using Python FastAPI and FFmpeg.

This project is composed of the following parts:

- **flash-converter-ws**: FastAPI web service that converts video to MP3.
- **flash-converter-tasks**: Celery worker that processes the video conversion tasks.
- **flash-converter-demo**: a demo of some advanced features of Video/Audio procession using AI models.

A part is a standalone project that can be run independently.

## Development

### Prerequisites

- Python 3.8
- Docker
- Docker Compose
- FFmpeg
- Redis

### Running the project

Open the `[docker-compose.yaml](docker-compose.yaml)` file and set the environment variables for the services.

```bash
docker-compose up
```

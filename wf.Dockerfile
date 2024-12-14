FROM python:3.12-slim-bullseye

LABEL authors="Laurent LAPORTE <laurent.laporte.pro@gmail.com" \
      description="Run Celery application in a container" \
      version="0.0.1"

ARG APP_USER=batman
ARG APP_GROUP=superheroes
ARG APP_HOME=/app
ARG APP_UPLOADS=/app/uploads

COPY wf.requirements.txt requirements.txt
COPY flash-converter-wf/src ${APP_HOME}

RUN echo "DEBUG: Python version: $(python3 --version)" && \
    echo "DEBUG: Pip version: $(python3 -m pip --version)" && \
    echo "INFO: Install ffmpeg" && \
    apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    echo "INFO: Install the application dependencies" && \
    python3 -m pip --no-cache-dir install --upgrade pip && \
    python3 -m pip --no-cache-dir install -r requirements.txt && \
    echo "INFO: Create a non-root user to run the application" && \
    groupadd --gid 1000 ${APP_GROUP} && \
    useradd --uid 1000 --gid ${APP_GROUP} --shell /bin/bash --create-home ${APP_USER} && \
    chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME} && \
    mkdir -p ${APP_UPLOADS} && \
    chown -R ${APP_USER}:${APP_GROUP} ${APP_UPLOADS} && \
    echo "INFO: Cleanup" && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


USER ${APP_USER}

WORKDIR ${APP_HOME}

CMD [ "celery", "--app=flash_converter_wf.server.celery_app", "worker", "--loglevel=info", "-Q", "default,voice,audio,subtitle" ]

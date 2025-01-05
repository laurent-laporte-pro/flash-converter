# Flash Converter UI

Flash Converter UI is a web application built with React and TypeScript that allows users to upload, process,
and manage video tasks.

## Features

- Upload videos for processing
- View the status of video tasks
- Download processed videos (with subtitles)
- Cancel or delete video tasks

## Technologies Used

- TypeScript
- JavaScript
- React
- npm
- Vite and Vitest
- Prettier
- ESLint

## Getting Started

### Prerequisites

The following software is required to run and develop the Flash Converter UI:

- Node.js (v14 or higher)
- npm (v6 or higher)

The following software is required to run the Flash Converter UI:

- Redis server: Redis server to store the video tasks.
- RabbitMQ server: RabbitMQ server to communicate with the Flash Converter Workflow.
- [Flash Converter Workflow](../flash-converter-wf/README.md): Flash Converter Workflow to process the video tasks.
- [Flash Converter API](../flash-converter-ws/README.md): Flash Converter API to manage the video tasks.

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/laurent-laporte-pro/flash-converter.git
   cd flash-converter/flash-converter-ui
   ```

2. Install the dependencies:

   ```shell
   npm install
   ```

## Usage

Follow the bellows steps to start the Flash Converter Workflow, API, and UI:

1. Run a RabbitMQ server on the default port (5672).

2. Run a Redis server on the default port (6379).

3. Start the Flash Converter Workflow: activate the virtual environment of `flash-converter-wf`
   and run the following command:

   ```shell
   python -m celery -A flash_converter_wf.server.celery_app worker -l info -Q default,voice,audio,subtitle
   ```

4. Start the Flash Converter API: activate the virtual environment of `flash-converter-api`
   and run the following command:

   ```shell
   python -m uvicorn flash_converter.ws.api:app --reload 
   ```

   The application will be available at `http://127.0.0.1:8000`.

5. Start the Flash Converter UI: run the following command:

   ```shell
   npm run dev
   ```

   The application will be available at `http://localhost:3000`.


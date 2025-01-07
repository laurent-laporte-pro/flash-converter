# This Dockerfile is used to build and serve the web application (a React app) using Nginx.
# The build process is done in a multi-stage build, where the first stage is used to build the React app
# and the second stage is used to serve the app using Nginx.

FROM node:lts-alpine3.21 as build

LABEL authors="Laurent LAPORTE <laurent.laporte.pro@gmail.com>" \
      description="Build Flash Converter UI app (React app) using Node." \
      version="0.1.0" \
      stage="build"

WORKDIR /app

# Install the required packages
COPY flash-converter-ui/package.json .
COPY flash-converter-ui/package-lock.json .

RUN npm install

# Build the client application using Vite
COPY flash-converter-ui/public public
COPY flash-converter-ui/src src
COPY flash-converter-ui/index.html .
COPY flash-converter-ui/tsconfig.app.json .
COPY flash-converter-ui/tsconfig.json .
COPY flash-converter-ui/tsconfig.node.json .
COPY flash-converter-ui/vite.config.ts .

RUN npm run build  # output in /app/dist

# Install and run nginx

FROM nginx:1.27-alpine as run

LABEL authors="Laurent LAPORTE <laurent.laporte.pro@gmail.com>" \
      description="Run Flash Converter UI app (React app) using Nginx." \
      version="0.1.0" \
      stage="run"

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80/tcp

CMD ["nginx", "-g", "daemon off;"]

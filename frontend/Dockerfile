# # build stage
FROM node:18-bullseye as build-stage
ARG BACKEND_HOST

WORKDIR /app
RUN apt update -y && apt upgrade -y
RUN apt install gettext -y

COPY package.json ./
COPY src src
COPY public public

RUN BACKEND_HOST=${BACKEND_HOST} && echo $BACKEND_HOST
RUN BACKEND_HOST=${BACKEND_HOST} && envsubst '${BACKEND_HOST}' < src/utils/config_template.js > src/utils/config.js
RUN npm install --legacy-peer-deps
RUN npm run build

# # production stage
FROM nginx:stable-alpine as production-stage
ARG GPU_LOCALHOST

COPY --from=build-stage /app/build /usr/share/nginx/html

COPY nginx/nginx_template.conf /etc/nginx/nginx_template.conf
COPY nginx/nginx_configure.sh /etc/nginx/nginx_configure.sh

WORKDIR /etc/nginx
RUN GPU_LOCALHOST=${GPU_LOCALHOST} && echo $GPU_LOCALHOST
RUN GPU_LOCALHOST=${GPU_LOCALHOST} && envsubst '${GPU_LOCALHOST}' < nginx_template.conf > nginx.conf

CMD nginx -g 'daemon off;'

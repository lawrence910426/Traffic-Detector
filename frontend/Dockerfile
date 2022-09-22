ARG BACKEND_HOST

# # build stage
FROM node:18-bullseye as build-stage
WORKDIR /app
RUN apt update -y && apt upgrade -y
RUN apt install gettext -y

# # build stage
COPY package.json ./
COPY src src
COPY public public

RUN npm install --legacy-peer-deps
RUN npm run build

# # production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/build /usr/share/nginx/html

COPY nginx/nginx_template.conf /etc/nginx/nginx_template.conf
COPY nginx/nginx_vars.sh /etc/nginx/nginx_vars.sh

CMD ["/bin/sh", "/etc/nginx/nginx_vars.sh", "&", "nginx", "-g", "daemon off;"]

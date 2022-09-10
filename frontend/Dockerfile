# # build stage
FROM node:18-bullseye as build-stage
WORKDIR /app
RUN apt update -y && apt upgrade -y

# # build stage
COPY package.json ./
COPY src src
COPY public public

RUN npm install --legacy-peer-deps
RUN npm run build

# # production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/build /usr/share/nginx/html
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]

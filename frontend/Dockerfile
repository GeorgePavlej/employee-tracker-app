# Stage 1: Build
FROM node:18.18-alpine AS build-stage

WORKDIR /app

COPY app/package*.json ./

RUN npm install --verbose --no-audit --legacy-peer-deps

COPY app ./

ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false

RUN echo "API URL for production: $VUE_APP_API_URL"
RUN node --max_old_space_size=4096 node_modules/.bin/vue-cli-service build

# Stage 2: Serve with Nginx
FROM nginx:alpine AS runtime

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY app/nginx.conf /etc/nginx/conf.d/default.conf

RUN echo "window.API_URL_DEBUG = '${VUE_APP_API_URL}';" > /usr/share/nginx/html/env-config.js

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


# Stage 1: Build
FROM node:18-alpine AS build-stage

WORKDIR /app

COPY app/package*.json ./

RUN npm install

COPY app ./

RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine AS runtime


COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


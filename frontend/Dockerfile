# Stage 1: Build
FROM node:18.18-alpine AS build-stage

WORKDIR /app

COPY app/package*.json ./

# Install dependencies with more verbose output and increased timeout
RUN npm install --verbose --no-audit --legacy-peer-deps

COPY app ./

# Set environment variables for production build
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false

# Print the API URL and run the production build script
RUN echo "API URL for production: $VUE_APP_API_URL"
RUN npm run build:production

# Stage 2: Serve with Nginx
FROM nginx:alpine AS runtime

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY app/nginx.conf /etc/nginx/conf.d/default.conf

# Create a file to help debug the environment at runtime
RUN echo "window.API_URL_DEBUG = '${VUE_APP_API_URL}';" > /usr/share/nginx/html/env-config.js

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


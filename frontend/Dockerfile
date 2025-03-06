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

# Run the build with increased memory and more verbose output
RUN node --max_old_space_size=4096 node_modules/.bin/vue-cli-service build

# Stage 2: Serve with Nginx
FROM nginx:alpine AS runtime

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


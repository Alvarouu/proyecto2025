# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build --prod

# Usar nginx
FROM nginx:alpine
COPY --from=builder /app/dist/angular/browser /usr/share/nginx/html

# Renombrar index.csr.html a index.html si es necesario
RUN mv /usr/share/nginx/html/index.csr.html /usr/share/nginx/html/index.html
FROM node:20-alpine

# Install a simple web server
RUN npm install -g http-server

# Create a simple index.html as placeholder
RUN mkdir -p /app
RUN echo '<!DOCTYPE html><html><head><title>Todo App</title></head><body><h1>Todo App Frontend</h1><p>Backend is running at <a href="/api/health">/api/health</a></p></body></html>' > /app/index.html

WORKDIR /app

EXPOSE 3000

CMD ["http-server", ".", "-p", "3000"]
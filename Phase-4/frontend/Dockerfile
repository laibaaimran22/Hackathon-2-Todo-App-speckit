# Use Node.js 20 as the base image
FROM node:20-alpine AS builder

# Install system dependencies for native modules
RUN apk add --no-cache python3 make g++

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Set environment variables for build time (with correct values for Kubernetes)
ENV NEXT_PUBLIC_BACKEND_URL="http://todo-app-backend:8000"
ENV NEXT_PUBLIC_API_BASE_URL="http://todo-app-backend:8000"
ENV DATABASE_URL="postgresql://dummy:dummy@dummy:5432/dummy"
ENV JWT_SECRET="dummy_secret"
ENV BETTER_AUTH_SECRET="dummy_secret"
ENV COHERE_API_KEY="dummy_key"

# Build the application
RUN npx next build

# Production stage - copy the built application
FROM node:20-alpine AS runner

# Install system dependencies needed at runtime
RUN apk add --no-cache python3

# Set working directory
WORKDIR /app

# Copy package files
COPY --from=builder /app/package*.json ./

# Install only production dependencies
RUN npm install --only=production

# Copy the built Next.js app from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

# Expose port
EXPOSE 3000

# Start the standalone Next.js application
CMD ["node", ".next/standalone/server.js"]
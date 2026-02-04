FROM node:20-alpine AS builder

WORKDIR /app

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install dependencies with longer timeout
RUN npm ci --prefer-offline --no-audit 2>&1 || npm install --legacy-peer-deps

# Copy source
COPY . .

# Provide dummy DATABASE_URL for build
ARG DATABASE_URL=postgresql://dummy:dummy@localhost/dummy
ENV DATABASE_URL=$DATABASE_URL

# Build
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy only built files and node_modules needed for production
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["npm", "start"]
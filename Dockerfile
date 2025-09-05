# Base stage with common dependencies
FROM python:3.11-slim AS base

# Install Node.js (for React frontend)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install frontend dependencies
RUN cd frontend && npm install

ARG APP_VERSION=unknown
ENV APP_VERSION=$APP_VERSION


# Development stage
FROM base AS development
ENV NODE_ENV=development
EXPOSE 8080 5173
CMD cd /app && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 \
    --reload --reload-exclude "frontend/node_modules/.vite/*" \
    --reload-exclude "frontend/node_modules/.vite/deps_temp*" & \
    cd /app/frontend && npm run dev -- --host 0.0.0.0 --port 5173

# Production stage
FROM base AS production
ENV NODE_ENV=production
ENV PORT=8080
EXPOSE 8080
RUN cd frontend && npm run build && cp -r dist ../backend/
CMD cd /app && python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT

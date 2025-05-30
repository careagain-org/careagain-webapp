FROM python:3.12-slim

WORKDIR /app

ARG NODE_VERSION=18.x

# Install necessary tools, Node.js, and unzip
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gnupg \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y xclip && \
    rm -rf /var/lib/apt/lists/*

# Install CA certs and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Verify Node.js installation
RUN node --version && npm --version

# Create reflex user
RUN adduser --disabled-password --home /app reflex

# Set up Python environment
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application files
COPY --chown=reflex:reflex . /app

# Move .build-env to .env if it exists
RUN if [ -f .build-env ]; then mv .build-env .env; fi

# Set permissions
RUN chown -R reflex:reflex /app

# Switch to reflex user
USER reflex

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize Reflex
RUN reflex init

# Remove .env file after reflex init
RUN rm -f .env

# Ensure all environment variables are set
ENV PATH="/app/.venv/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
ENV NODE_PATH="/usr/lib/node_modules"
ENV REFLEX_DB_URL="sqlite:///reflex.db"

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

# Always apply migrations before starting the backend.
CMD ["sh", "-c", "reflex db migrate && reflex run --env prod --backend-only"]
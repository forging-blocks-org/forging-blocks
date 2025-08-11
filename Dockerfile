FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# These environment variables are good, but we'll also add explicit config commands
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

WORKDIR /app

# Install build dependencies for psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    # Add any other build dependencies your project might need here
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir "poetry==1.7.1"

# Explicitly configure Poetry to not create virtual environments
# and to install dependencies directly into the system Python's site-packages.
# This prevents the "Recreating virtualenv" issue.
RUN poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

# Copy your project files into the container
COPY . .

# Install project dependencies using Poetry.
# Since virtualenvs.create is false, these will be installed globally.
RUN poetry install --with dev --no-interaction

# Set PYTHONPATH to include your application's source directory
ENV PYTHONPATH=/app/src

# Define the entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]

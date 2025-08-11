#!/usr/bin/env bash
set -e

# This script is the entry point for running the HTTP server in a Docker container.
# It waits for the PostgreSQL database to be ready, runs migrations, and starts the server.

EXAMPLE=${1:-${EXAMPLE:-tasker_primitive_obsession}}

./scripts/wait_to_it.sh postgres 5432 ./scripts/migrate.sh "$EXAMPLE"

# # Check that the migration script exists
# if [[ ! -x ./scripts/migrate.sh ]]; then
#   echo "Error: ./scripts/migrate.sh not found or not executable."
#   exit 1
# fi

# Run migrations for the current example
# ./scripts/migrate.sh "$EXAMPLE"

# Check that the main app module exists (python import path check)
MAIN_MODULE="examples.$EXAMPLE.src.presentation.http.main"
PYTHON_MAIN_PATH="examples/$EXAMPLE/src/presentation/http/main.py"
if [[ ! -f "$PYTHON_MAIN_PATH" ]]; then
  echo "Error: Main module $PYTHON_MAIN_PATH not found."
  exit 1
fi

echo "Starting the HTTP server for $EXAMPLE..."
exec poetry run uvicorn "$MAIN_MODULE:app" --host 0.0.0.0 --port 8000 --reload

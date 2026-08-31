#!/bin/sh
set -e

MODEL_PATH="app/models/mango_advisory_model.pkl"
MODEL_URL="https://github.com/udananirmal12-cell/MangoCare/raw/refs/heads/main/Backend/app/models/mango_advisory_model.pkl"

echo "Downloading advisory model..."

python - <<'PY'
import os
import urllib.request

url = "https://github.com/udananirmal12-cell/MangoCare/raw/refs/heads/main/Backend/app/models/mango_advisory_model.pkl"
destination = "app/models/mango_advisory_model.pkl"

os.makedirs(os.path.dirname(destination), exist_ok=True)
urllib.request.urlretrieve(url, destination)

print("Advisory model downloaded successfully.")
PY

echo "Starting MangoCare backend..."

exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
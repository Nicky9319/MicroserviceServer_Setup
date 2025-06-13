#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check for docker-compose.yml or .yaml and run docker-compose up if found
if [[ -f "$PROJECT_ROOT/docker-compose.yml" || -f "$PROJECT_ROOT/docker-compose.yaml" ]]; then
    sudo docker-compose -f "$PROJECT_ROOT/docker-compose.yml" up -d 2>/dev/null || \
    sudo docker-compose -f "$PROJECT_ROOT/docker-compose.yaml" up -d
else
    echo "docker-compose.yml or docker-compose.yaml not found in $PROJECT_ROOT. Skipping docker-compose up."
fi

# Check .env file for syntax errors
ENV_PATH="$PROJECT_ROOT/.env"
if [[ -f "$ENV_PATH" ]]; then
    LINENUM=0
    while IFS= read -r line; do
        LINENUM=$((LINENUM+1))
        [[ -z "$line" || "$line" =~ ^# ]] && continue
        if ! [[ "$line" == *=* ]]; then
            echo "WARNING: .env file syntax error at line $LINENUM: $line"
        fi
    done < "$ENV_PATH"
fi

cd "$PROJECT_ROOT"

# Start services from services.json
SERVICES_JSON="$PROJECT_ROOT/services.json"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python3.12"

if [[ -f "$SERVICES_JSON" ]]; then
    python3 -c "
import json, os, subprocess, shlex
with open('$SERVICES_JSON') as f:
    try:
        services = json.load(f)
    except Exception as e:
        print(f'Error reading $SERVICES_JSON: {e}')
        services = []
for service in services:
    folder = service.get('ServiceFolderName')
    filename = service.get('ServiceFileName')
    if not folder or not filename:
        continue
    service_path = os.path.join('$PROJECT_ROOT', folder, filename)
    if not os.path.exists(service_path):
        print(f'Service file {service_path} not found. Skipping.')
        continue
    cmd = f'$VENV_PYTHON {folder}/{filename} &'
    print(f'Starting: {cmd}')
    subprocess.Popen(shlex.split(f'$VENV_PYTHON {folder}/{filename}'))
" 
else
    echo "$SERVICES_JSON not found."
fi

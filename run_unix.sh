#!/usr/bin/env bash
set -e
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Starting API at http://127.0.0.1:8000/docs"
uvicorn src.app:app --reload

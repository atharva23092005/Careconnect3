#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python init_db.py

echo "Build complete!"

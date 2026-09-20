#!/bin/bash
set -e

APP_DIR="/home/ubuntu/flask-cicd-ec2"
cd "$APP_DIR"

echo "=== [1/3] Pulling latest changes from Git main ==="
git config --global --add safe.directory "$APP_DIR"
git fetch origin main
git reset --hard origin/main

echo "=== [2/3] Updating Python virtual environment ==="
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [3/3] Restarting flaskapp.service ==="
sudo systemctl restart flaskapp

# Verify that service is active
if sudo systemctl is-active --quiet flaskapp; then
    echo "? Deployment Successful! Service is active and running."
else
    echo "? Deployment Failed: flaskapp service is not active."
    sudo journalctl -u flaskapp -n 20 --no-pager
    exit 1
fi

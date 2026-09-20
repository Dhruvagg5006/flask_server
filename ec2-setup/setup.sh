#!/bin/bash
set -e

echo "======================================================="
echo "  AWS EC2 Setup: Flask CI/CD Server Initialization"
echo "======================================================="

# 1. Update system packages
echo ">>> [1/5] Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# 2. Install Python 3, venv, pip, git, and curl
echo ">>> [2/5] Installing Python 3, venv, Git, and utilities..."
sudo apt-get install -y python3 python3-pip python3-venv git curl

# 3. Configure Git safe directory
git config --global --add safe.directory /home/ubuntu/flask-cicd-ec2

APP_DIR="/home/ubuntu/flask-cicd-ec2"
if [ ! -d "$APP_DIR" ]; then
    echo "------------------------------------------------------------------"
    echo "??  Directory $APP_DIR does not exist yet."
    echo "Please clone your repository first, then re-run this script:"
    echo "    git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO>.git $APP_DIR"
    echo "------------------------------------------------------------------"
    exit 1
fi

cd "$APP_DIR"

# 4. Create and configure virtual environment
echo ">>> [3/5] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Configure systemd service
echo ">>> [4/5] Installing systemd service unit..."
sudo cp "$APP_DIR/ec2-setup/flaskapp.service" /etc/systemd/system/flaskapp.service

echo ">>> [5/5] Enabling and starting flaskapp service..."
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl restart flaskapp

# Check status
echo ""
echo "======================================================="
echo "? EC2 Environment Setup Completed Successfully!"
echo "Service status:"
sudo systemctl status flaskapp --no-pager
echo ""
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com || curl -s ifconfig.me || echo "<YOUR-EC2-PUBLIC-IP>")
echo "Access your live Flask application at: http://$PUBLIC_IP:5000"
echo "======================================================="

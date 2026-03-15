#!/bin/bash

# Cyber Agent Installation Script
# Must be run as root

if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit 1
fi

echo "Installing Cyber Agent..."

INSTALL_DIR="/opt/cyber-agent"
CONFIG_DIR="/etc/cyber-agent"
LOG_DIR="/var/log"

# Create directories
mkdir -p "$INSTALL_DIR/src"
mkdir -p "$CONFIG_DIR"

# Copy source code
echo "Copying source files..."
cp -r ../src/* "$INSTALL_DIR/src/"
cp ../config/settings.yaml "$CONFIG_DIR/"

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r ../requirements.txt

# Install Systemd Service
echo "Installing systemd service..."
cp cyber-agent.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable cyber-agent
systemctl start cyber-agent

echo "Installation complete. Cyber Agent is running."
echo "Check logs at /var/log/cyber-agent.log"

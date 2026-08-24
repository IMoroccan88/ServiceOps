#!/bin/bash

# Stop the script immediately if any command fails.
set -e

# Move into the ServiceOps application directory.
cd /opt/ServiceOps

# Pull the newest application code from GitHub.
git pull origin master

# Activate the ServiceOps Python virtual environment.
source .venv/bin/activate

# Make sure this server has every Python package required by the application.
pip install -r requirements.txt

# Restart ServiceOps so Gunicorn loads the new code.
sudo systemctl restart serviceops

# Show the current status of ServiceOps.
sudo systemctl status serviceops --no-pager

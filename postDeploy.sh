#!/bin/bash
set -e

rsync -a --delete \
  --exclude '.venv' \
  --exclude '.git' \
  /opt/ServiceOps-deploy/ /opt/ServiceOps/

chown -R serviceops:serviceops /opt/ServiceOps

sudo -u serviceops /opt/ServiceOps/.venv/bin/pip install -r /opt/ServiceOps/requirements.txt

systemctl restart serviceops

systemctl is-active --quiet serviceops

curl --fail http://127.0.0.1:5000/health

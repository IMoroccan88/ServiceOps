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

# Give ServiceOps several chances to become ready.
# Try once per second for up to 15 seconds.
for attempt in {1..15}
do
    if curl --fail --silent http://127.0.0.1:5000/health > /dev/null
    then
        echo "ServiceOps health check passed."
        exit 0
    fi

    echo "Waiting for ServiceOps to become ready... attempt $attempt/15"
    sleep 1
done

# If we reach this point, ServiceOps never became healthy.
echo "ERROR: ServiceOps failed health check."
exit 1

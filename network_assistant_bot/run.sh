#!/usr/bin/env bash
export FLASK_ENV=development
set -xe
ngrok http 5000 -bind-tls=true -config /opt/config/ngrok.yaml -log=stdout > /dev/null &
sleep 10
python nabot.py &
bash

#!/usr/bin/env bash
REPO_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
NAME="nabot"

docker stop $NAME > /dev/null &
docker rm -f $NAME > /dev/null &
docker run -itd \
--name $NAME \
-p 5001:4040 \
-p 5002:5000 \
-v $REPO_DIR/network_assistant_bot:/network_assistant_bot \
-v $REPO_DIR/helpers:/network_assistant_bot/helpers \
-v $REPO_DIR/config:/opt/config \
-e PYTHONPATH=/network_assistant_bot/ \
--entrypoint /network_assistant_bot/run.sh \
nabot:latest $@

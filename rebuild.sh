#!/usr/bin/env bash
docker container stop nabot && docker container rm nabot && docker image rm nabot
docker build -t nabot .
#!/bin/bash
CONFIG_PATH=$1
# Run agent in docker container
export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"
export CONFIG_PATH=$CONFIG_PATH
docker compose --project-directory docker/ up --build
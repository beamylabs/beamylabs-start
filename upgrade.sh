#!/bin/bash

cd "${0%/*}" || { printf "Can't cd to script dir?!\n"; exit 1; }

composef="docker-compose-full-system.yml"

if [ ! -f "$composef" ]; then
  printf "%: file not found\n" "$composef"
  exit 1
fi

if [ -z "$NODE_NAME" ]; then
  NODE_NAME="$(scripts/resolve-ip.sh eth0)"
fi
export NODE_NAME

docker-compose -f "$composef" down
docker-compose -f "$composef" pull
docker-compose -f "$composef" up -d

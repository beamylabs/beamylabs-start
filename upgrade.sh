#!/bin/sh

cd "${0%/*}"

if [ -z "${SIGNALBROKER_IP}" ]; then
  printf "SIGNALBROKER_IP not set, using default values as SIGNALBROKER_IP=\"$(scripts/resolve-ip.sh wlan0)\"\n"
  export SIGNALBROKER_IP=$(scripts/resolve-ip.sh wlan0)
fi

if [ -z "${NODE_NAME}" ]; then
  printf "NODE_NAME not set, using default values as NODE_NAME=\"$(scripts/resolve-ip.sh eth0)\"\n"
  export NODE_NAME=$(scripts/resolve-ip.sh eth0)
fi

docker-compose -f docker-compose-full-system.yml down
docker-compose -f docker-compose-full-system.yml pull
docker-compose -f docker-compose-full-system.yml up -d

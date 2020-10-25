#!/bin/sh

cd "${0%/*}"

SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml down
SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml pull
SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml up -d

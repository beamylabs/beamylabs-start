#!/bin/sh

cd "${0%/*}"

NODE_NAME=$(scripts/resolve-ip.sh eth0) SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml down
NODE_NAME=$(scripts/resolve-ip.sh eth0) SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml pull
NODE_NAME=$(scripts/resolve-ip.sh eth0) SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml up -d

#!/bin/bash
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml down
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml pull
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml up
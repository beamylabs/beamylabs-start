#!/bin/bash

scriptd="$(cd &>/dev/null -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if ! cd "$scriptd"; then
  printf "Can't cd to script dir '%s'?!\n" "$scriptd"
  exit 1
fi

composef="docker-compose-full-system.yml"

if [ ! -f "$composef" ]; then
  printf "%: file not found\n" "$composef"
  exit 1
fi

if [ -z "$NODE_NAME" ]; then
  NODE_NAME="$(scripts/resolve-ip.sh eth0)"
fi
export NODE_NAME

rm -f envfile
touch envfile
# trigger-upgrade.sh might pass us an env file
if [ -n "$1" ]; then
  printf "tags from passed envfile:\n"
  cat "$1"
  mv -f "$1" envfile
else
  printf "no envfile passed.\n"
fi

# for any unset *_TAG env vars, the docker-compose yml falls back to "latest"

if ! docker-compose --env-file envfile -f docker-compose-full-system.yml pull; then
  printf "upgrade aborted, some non-existent tag?\n"
  exit 1
fi

docker-compose --env-file envfile -f docker-compose-full-system.yml down
docker-compose --env-file envfile -f docker-compose-full-system.yml up -d

rpi=
grep &>/dev/null -i "raspberry" /sys/firmware/devicetree/base/model && rpi="rpi"

if [ -n "$rpi" ]; then
  # restarting to ensure that we're running the latest version of
  # scripts/trigger-upgrade.sh
  sudo systemctl restart beamylabs-upgrade
fi

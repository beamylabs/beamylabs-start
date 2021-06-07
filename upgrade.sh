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

# Upgrade docker if we're on a Raspberry Pi and version < 20.10.8
# We should be run as user "pi" and assume we can do password-less sudo.
if grep -qi "raspberry" /sys/firmware/devicetree/base/model; then
  # Make apt-update not exit when a repo changes suite (buster changed from
  # stable to oldstable in August 2021). Required for the get-docker.sh script
  # to complete, but done here because seems useful to have in place in case of
  # other upgrades.
  printf 'Acquire::AllowReleaseInfoChange::Suite "1";\n' \
   | sudo tee >/dev/null /etc/apt/apt.conf.d/99beamy-allowchangesuite

  v="$(docker version -f "{{.Server.Version}}")"
  va="${v%%.*}"
  vb="${v#*.}"; vb="${vb%%.*}"; vb="${vb#0}"
  vc="${v##*.}"; vc="${vc#0}"
  printf "docker version: %d,%d,%d\n" "$va" "$vb" "$vc"
  if (( va < 20 || (va == 20 && (vb < 10 || (vb == 10 && vc < 8))) )); then
    curl -fsSL -o get-docker.sh https://get.docker.com
    sh ./get-docker.sh
  else
    printf "docker upgrade not needed\n"
  fi
fi

docker-compose --env-file envfile -f docker-compose-full-system.yml up -d

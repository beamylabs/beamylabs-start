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

docker-compose -f "$composef" pull
docker-compose -f "$composef" up -d

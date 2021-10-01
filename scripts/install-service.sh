#!/bin/bash

cd "${0%/*}"

if [[ "$EUID" != 0 ]]; then
  printf "Please give me root privileges by running me with sudo or doas.\n"
  exit 1
fi

BEAMYHOME="$(realpath ..)"
if [[ -z "$BEAMYHOME" ]]; then
  printf "Could not get location of beamylabs-start.\n"
  exit 1
fi

BEAMYUSER="${SUDO_USER:-${DOAS_USER}}"
if [[ -z "$BEAMYUSER" ]]; then
  printf "Could not get real user running the script.\n"
  exit 1
fi

sed >beamylabs-upgrade.service \
    -e "s,@BEAMYHOME@,$BEAMYHOME,g" \
    -e "s,@BEAMYUSER@,$BEAMYUSER,g" \
    beamylabs-upgrade.service.tmpl

set -x
cp -af beamylabs-upgrade.service /etc/systemd/system/

systemctl daemon-reload
systemctl restart beamylabs-upgrade
systemctl enable beamylabs-upgrade

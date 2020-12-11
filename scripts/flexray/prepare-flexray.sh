#!/bin/sh
set -eu

serial="${1:-}"

echo "When propted for (yes/no), type yes and hit enter. When requested for password, hit enter"

if [ -z "$serial" ]; then
  echo >/dev/stderr "you need to provide the serial of the flexray device as in ./prepare-flexray 18101016"
  exit 0
fi

hostname=mx4-t30-$serial

scp flexray2ip.new flexray-forward.service root@$hostname:
ssh root@$hostname bash <<'ENDSSH'

chmod 777 flexray-forward.service
cp flexray-forward.service /etc/systemd/system/
systemctl start flexray-forward
systemctl enable flexray-forward

ENDSSH


echo "use this $hostname in your interfaces.json"

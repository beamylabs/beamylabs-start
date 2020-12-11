#!/bin/sh
set -eu

hostname="${1:-}"

echo "When propted for (yes/no), type yes and hit enter. When requested for password, hit enter"

if [ -z "$hostname" ]; then
  echo >/dev/stderr "you need to provide the ip or the hostname $0 192.168.4.1 or $0 hostname"
  exit 0
fi

scp flexray2ip.new flexray-forward.service root@$hostname:
ssh root@$hostname bash <<'ENDSSH'

chmod 777 flexray-forward.service
cp flexray-forward.service /etc/systemd/system/
systemctl start flexray-forward
systemctl enable flexray-forward

ENDSSH

echo "\nTAKE A NOTE OF THIS HOSTNAME: $hostname IT SHOULD BE ADDED TO interfaces.json"

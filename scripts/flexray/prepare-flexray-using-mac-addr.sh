#!/bin/sh
set -eu

macaddr="${1:-}"

echo "When propted for (yes/no), type yes and hit enter. When requested for password, hit enter"

if [ -z "$macaddr" ]; then
  echo >/dev/stderr "you need to provide the mac address of the flexray device as in ./prepare-flexray-mac-addr 01:1c:2e:10:00:12"
  exit 0
fi

hostname=`arp -a | grep "04:1b:94:00:28:86" | awk '{print $2}' | sed 's/[()]//g'`

scp flexray2ip.new flexray-forward.service root@$hostname:
ssh root@$hostname bash <<'ENDSSH'

chmod 777 flexray-forward.service
cp flexray-forward.service /etc/systemd/system/
systemctl start flexray-forward
systemctl enable flexray-forward

ENDSSH


echo "use this $hostname in your interfaces.json"

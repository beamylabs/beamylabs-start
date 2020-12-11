#!/bin/sh
set -eu

macaddr="${1:-}"

if [ -z "$macaddr" ]; then
  echo >/dev/stderr "you need to provide the mac address of the flexray device as in $0 01:1c:2e:10:00:12"
  exit 0
fi

hostname=`arp -a | grep $macaddr | awk '{print $2}' | sed 's/[()]//g'`

./prepare-flexray.sh $hostname

#!/bin/sh
set -eu

macaddr="${1:-}"

if [ -z "$macaddr" ]; then
  echo >/dev/stderr "you need to provide the mac address of the flexray device as in $0 01:1c:2e:10:00:12"
  exit 0
fi

hostname=`nmap -sP 192.168.1.0/24 >/dev/null && arp -an | grep $macaddr | awk '{print $2}' | sed 's/[()]//g'`

if [ -z "$hostname" ]; then
  echo >/dev/stderr "failed resoling ip/hostname, try another way"
  exit 0
fi

./prepare-flexray.sh $hostname

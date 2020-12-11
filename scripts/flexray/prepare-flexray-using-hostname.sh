#!/bin/sh
set -eu

serial="${1:-}"

if [ -z "$serial" ]; then
  echo >/dev/stderr "you need to provide the serial of the flexray device as in $0 18101016"
  exit 0
fi

hostname=mx4-t30-$serial

./prepare-flexray.sh $hostname


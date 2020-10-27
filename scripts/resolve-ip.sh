#!/bin/sh
set -eu

# defaultip="192.168.4.1"
defaultip=""

iface="${1:-}"

if [ -z "$iface" ]; then
  echo >/dev/stderr "no interface given"
  echo "$defaultip"
  exit 0
fi

found="$(ifconfig "$iface" | sed -E -n "s/^[[:space:]]*inet (([0-9]+\.){3}[0-9]+).*/\1/p")"
case "$found" in
  ""|127.0.0.1)
    ip="$defaultip"
    ;;
  *)
    ip="$found"
    ;;
esac

echo "$ip"

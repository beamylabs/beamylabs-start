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

# ip addr show "$iface"
if type "ip" > /dev/null; then
    cmd="ip addr show"
else
    cmd="ifconfig"
fi


found="$($cmd "$iface" | sed -E -n "s/^[[:space:]]*inet (([0-9]+\.){3}[0-9]+).*/\1/p")"
case "$found" in
  ""|127.0.0.1|169.254.*)
    ip_addr="$defaultip"
    ;;
  *)
    ip_addr="$found"
    ;;
esac

echo "$ip_addr"

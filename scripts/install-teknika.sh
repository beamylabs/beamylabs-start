#!/bin/bash

cd "${0%/*}"

if [[ "$EUID" != 0 ]]; then
  printf "Please give me root privileges by running me with sudo or doas.\n"
  exit 1
fi

TEKNIKABIN=/usr/local/bin/teknika

arch="$(uname -m)"
case "$arch" in
  x86_64|aarch64)
    cp -vaf teknika/teknika-"$arch" "$TEKNIKABIN"
    ;;
  armv7l)
    cp -vaf teknika/teknika-armhf "$TEKNIKABIN"
    ;;
  *)
    printf "your system arch %s is unknown\n" "$arch"
    exit 1
    ;;
esac

mkdir -p /etc/teknika
echo "PORT=51111" >/etc/teknika/instance1
echo "PORT=51112" >/etc/teknika/instance2

sed >/etc/systemd/system/teknika@.service \
    -e "s,@TEKNIKABIN@,$TEKNIKABIN,g" \
    teknika/teknika@.service.tmpl

systemctl daemon-reload
systemctl stop teknika@instance1 || true
systemctl stop teknika@instance1 || true
systemctl enable --now teknika@instance1
systemctl enable --now teknika@instance2

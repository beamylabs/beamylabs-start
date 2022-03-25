#!/bin/bash

cd "${0%/*}" || exit 1

if [[ "$EUID" != 0 ]]; then
  printf "Please give me root privileges by running me with sudo or doas.\n"
  exit 1
fi

TEKNIKABIN=/usr/local/bin/teknika

arch="$(uname -m)"
case "$arch" in
  x86_64|aarch64)
    archbin="teknika/teknika-$arch"
    ;;
  armv7l)
    archbin="teknika/teknika-armhf"
    ;;
  *)
    printf "your system arch %s is unknown\n" "$arch"
    exit 1
    ;;
esac
cp -vf --preserve=mode,timestamps "$archbin" "$TEKNIKABIN"

mkdir -p /etc/teknika
# We avoid overwriting any user changes to the ports
if ! grep -sq "^PORT=" /etc/teknika/instance1; then
  touch /etc/teknika/instance1
  printf >/etc/teknika/instance1 "PORT=51111\n"
fi
if ! grep -sq "^PORT=" /etc/teknika/instance2; then
  touch /etc/teknika/instance2
  printf >/etc/teknika/instance2 "PORT=51112\n"
fi

sed >/etc/systemd/system/teknika@.service \
    -e "s,@TEKNIKABIN@,$TEKNIKABIN,g" \
    teknika/teknika@.service.tmpl

systemctl daemon-reload
systemctl stop teknika@instance1 || true
systemctl stop teknika@instance2 || true
systemctl enable teknika@instance1
systemctl enable teknika@instance2
systemctl start teknika@instance1 || true
systemctl start teknika@instance2 || true

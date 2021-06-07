#!/bin/bash

inotifywait -m -r configuration/ -e create -e moved_to \
 | while read -r path _action file; do
  [[ "$file" != "upgrade" ]] && continue

  printf "* trigger by upgrade file, tags picked up from the file:\n"
  envf="$(mktemp -t upgrade-env.XXXX)"
  # filter out only legal env var/vals
  grep -E '^(BEAMYBROKER|GRPCWEBPROXY|BEAMYWEBCLIENT)_TAG="[a-zA-Z0-9][-.a-zA-Z0-9]{0,127}"$' "$path/$file"\
   | tee "$envf"

  printf "* git pull\n"
  git pull

  printf "* trying to upgrade system\n"
  ./upgrade.sh "$envf"
done

exit 0

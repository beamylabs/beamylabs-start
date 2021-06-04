#!/bin/bash

inotifywait -m -r configuration/ -e create -e moved_to \
  | while read -r path _action file; do
      if [[ "$file" = "upgrade" ]]; then
        echo "trying to upgrade system"
        envf="$(mktemp -t upgrade-env.XXXX)"
        # filter out only legal env var/vals
        grep >"$envf" -E '^(BEAMYBROKER|GRPCWEBPROXY|BEAMYWEBCLIENT)_TAG="[a-zA-Z0-9][-.a-zA-Z0-9]{0,127}"$' "$path/$file"
        git pull
        ./upgrade.sh "$envf"
      fi
    done
exit 0

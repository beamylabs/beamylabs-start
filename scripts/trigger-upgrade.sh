#!/bin/bash

inotifywait -m -r configuration/ -e create -e moved_to \
 | while read -r path _action file; do
  [[ "$file" != "upgrade" ]] && continue

  printf "* trigger by upgrade file, tags picked up from the file:\n"
  envf="$(mktemp -t upgrade-env.XXXXXX)"
  # pick up precisely the var/vars that we care about from the upgrade file
  pattern='^(BEAMYBROKER|BEAMYWEBCLIENT)_TAG="[a-zA-Z0-9][-.a-zA-Z0-9]{0,127}"$'
  grep -E -e "$pattern" "$path/$file" | tee "$envf"

  printf "* git pull\n"
  git pull

  printf "* trying to upgrade system\n"
  ./upgrade.sh "$envf"

  # The above upgrade.sh must be the last thing done here, as this script might
  # decide to restart the beamylabs-upgrade service (to ensure that latest
  # trigger-upgrade.sh is running).
done

exit 0

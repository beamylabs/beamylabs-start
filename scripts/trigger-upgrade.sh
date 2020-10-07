#!/bin/bash
inotifywait -m -r configuration/ -e create -e moved_to |
    while read path action file; do
        if [[ "$file" =~ upgrade$ ]]; then # time to upgrade
            echo "trying ot upgrade system"
            script/upgrade.sh
        fi
    done
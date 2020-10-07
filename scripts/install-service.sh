#!/bin/bash
#run this as sudo
cp beamylabs-upgrade.service /etc/systemd/system/
systemctl start beamylabs-upgrade
systemctl enable beamylabs-upgrade

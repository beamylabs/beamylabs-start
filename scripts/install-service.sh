#!/bin/bash
cp beamylabs-upgrade.service /etc/systemd/system/
sudo systemctl start beamylabs-upgrade
sudo systemctl enable beamylabs-upgrade

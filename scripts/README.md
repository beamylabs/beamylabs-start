# Note on scripts

## Debug the upgrade service

```
sudo systemctl start beamylabs-upgrade.service
sudo systemctl status beamylabs-upgrade.service
sudo systemctl stop beamylabs-upgrade.service

sudo journalctl -f -u beamylabs-upgrade
```

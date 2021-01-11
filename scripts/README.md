# Note on scripts

## Install
```
sudo ./install-service.sh
```

> these scripts assumes that the install location is `/home/pi/beamylabs-start` and that you are running on a system where the network interfaces are named `eth0` and `wlan0`.

### Debug
```
sudo systemctl start beamylabs-upgrade.service  
sudo systemctl status beamylabs-upgrade.service  
sudo systemctl stop beamylabs-upgrade.service  
```
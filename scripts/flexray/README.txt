Use one of these scripts to configure for your flexray node, make sure it's connected to the same network as this machine
Usually you can find the mac and/or the serial printed on the device.

Examples

using ip
./prepare-flexray.sh 192.168.1.82

using serial
./prepare-flexray-using-hostname.sh 01020304

using mac address
./prepare-flexray-using-mac-addr.sh 04:1c:64:01:28:86

using mac address option 2
In order to get this working do
-> sudo apt-get install nmap
./prepare-flexray-using-mac-addr-slow.sh 04:1c:64:01:28:86

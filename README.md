# Get started with BeamyBroker

## Start

Make sure you have `docker` and `docker-compose` installed, then

```bash
NODE_NAME=$(scripts/resolve-ip.sh eth0) SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml up
```
> On a generic setup `NODE_NAME` and `SIGNALBROKER_IP` will likely be set to the same value.

> `$(scripts/resolve-ip.sh eth0)` assumes that the interface for your main
> ethernet connection is called `eth0`. If that's not the case, you need to
> change `eth0` to the correct name (hint, find out using `ifconfig` or
> `ipconfig`).

> Some dated docker compose versions might show `ERROR: Invalid interpolation format for "command" option... `. If thats the case edit the [docker-compose-full-system.yml](docker-compose-full-system.yml) and replace [${SIGNALBROKER_IP:?Add SIGNALBROKER_IP to the .env file}](https://github.com/beamylabs/beamylabs-start/blob/master/docker-compose-full-system.yml#L34) with your ip resulting in `command: ./grpcwebproxy --backend_addr=192.x.x.x:50051...` manually.

> Running the above `docker-compose` command only needs to be done once. It
> persistant over system reboot, and will restart the containers upon reboot,
> over and over again.

Point your web browser at the machine running Beamybroker, an address like
`http://192.0.2.42:8080/`. If you are connected to a hosted WLAN Access Point
like `beamy-cafe42`, the address should be `http://192.168.4.1:8080/`.

> BEWARE: if you change your your interface settings you must restart by do doing [STOP](#stop)/[START](#start)

## Stop

```bash
NODE_NAME=$(scripts/resolve-ip.sh eth0) SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml down
```

## Upgrade

```bash
NODE_NAME=$(scripts/resolve-ip.sh eth0) SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml pull
```

## Inspiration

- [python](examples/grpc/python/README.md)
- [go](examples/grpc/go/README.md)
- [elixir](examples/grpc/elixir/car5g/README.md)
- [grpc-web](examples/grpc/grpc-web/README.md)

## Statistics and usage 

In order to understand usage of the product and it's enviroment it will try and send system information based on your interfaces.json and it's execution enviroment on start. The data is obfuscated and it is not distributed to any other party. Its sole purpose is the make the software better.

This is not mandatoy and can be disabled, however to keep us motivated we would please urge you not to disable this feature.

# Get started with BeamyBroker

## Start

Make sure you have `docker` and `docker-compose` installed, then

```bash
SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml up
```

> `$(scripts/resolve-ip.sh eth0)` assumes that the interface for your main
> ethernet connection is called `eth0`. If that's not the case, you need to
> change `eth0` to the correct name (hint, find out using `ifconfig` or
> `ipconfig`).

> Some dated docker compose versions might complain. If thats the case edit the [docker-compose-full-system.yml](docker-compose-full-system.yml) and replace [${SIGNALBROKER_IP:?Add SIGNALBROKER_IP to the .env file}](https://github.com/beamylabs/beamylabs-start/blob/master/docker-compose-full-system.yml#L34) with your ip resulting in `command: ./grpcwebproxy --backend_addr=192.x.x.x:50051...` manually.

> Running the above `docker-compose` command only needs to be done once. It
> persistant over system reboot, and will restart the containers upon reboot,
> over and over again.

Point your web browser at the machine running Beamybroker, an address like
`http://192.0.2.42:8080/`. If you are connected to a hosted WLAN Access Point
like `beamy-cafe42`, the address should be `http://192.168.4.1:8080/`.

## Stop

```bash
SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml down
```

## Upgrade

```bash
SIGNALBROKER_IP=$(scripts/resolve-ip.sh eth0) docker-compose -f docker-compose-full-system.yml pull
```

## Inspiration

- [python](examples/grpc/python/README.md)
- [go](examples/grpc/go/README.md)
- [elixir](examples/grpc/elixir/car5g/README.md)
- [grpc-web](examples/grpc/grpc-web/README.md)

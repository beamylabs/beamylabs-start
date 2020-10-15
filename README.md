# Get started with BeamyBroker

## Start
Make sure you have docker and docker-compose installed, then
```bash
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml up
```
> Some dated docker compose versions might complain. If thats the case edit the [docker-compose-full-system.yml](docker-compose-full-system.yml) and replace [${SIGNALBROKER_IP:?Add SIGNALBROKER_IP to the .env file}](https://github.com/beamylabs/beamylabs-start/blob/master/docker-compose-full-system.yml#L34) with your ip resulting in `command: ./grpcwebproxy --backend_addr=192.x.x.x:50051...` manually.



> This is persistant over system reboot, and it will restart on reboot over and over again

Point your webbrowser to the hosting machine example http://192.168.4.1:8080/ 

## Stop 
```bash
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml down
```

## Upgrade
```bash
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml pull
```

## Inspiration
- [python](examples/grpc/python/README.md)
- [go](examples/grpc/go/README.md)
- [elixir](examples/grpc/elixir/car5g/README.md)
- [grpc-web](examples/grpc/grpc-web/README.md)

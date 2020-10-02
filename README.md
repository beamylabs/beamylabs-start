# Get started with BeamyBroker

## Start
Make sure you have docker and docker-compose installed, then
```bash
SIGNALBROKER_IP=192.168.4.1 docker-compose -f docker-compose-full-system.yml up
```

Point you webbrowser to the hosting machine example http://192.168.4.1:8080/ 

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
- [go](examples/grpc/go)
- [elixir](examples/grpc/elixir)
- [grpc-web](examples/grpc/grpc-web)

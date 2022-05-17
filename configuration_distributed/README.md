# Get going with distributed setup

Distributed setup allows chaining devices enabling muliple physical ports. Typically a scenario would be where the host has not enough can ports. 

The connected devices can be of different kind. Linux machines can coexist with Raspberry pie:s.

## Setup

1. Make sure all nodes (machines) have license installed.
2. For all nodes - go to the beamylabs-start folder and do:
```bash
docker-compose down
NODE_NAME=xxx.xxx.xxx.xxx docker-compose up -d
```
> make sure to replace `xxx.xxx.xxx.xxx` with the proper ip of the machine.

3. Upload a valid configuration (or modify the configuration in this folder) to all the relevant nodes.
4. Using the web interface you should now se all namespaces listed on all machines.
5. Done!

## Valid interfaces.json
All node names must be prefixed with `node`. `slaveX.com` and `master.com` needs to be replaced with the proper ips's which are the same as were used when doing `docker-compose up` above.
```json
{
  "master_node": "node@master.com",
  "nodes": [
    {
      "node_name": "node@slave1.com",
      "default_namespace": "VirtualInterface",
      "chains": [
        {
          ...
        }
      ],
      "gateway": {
        "gateway_pid": "gateway_pid",
        "tcp_socket_port": 4041
      },
      "auto_config_boot_server": {
        "port": 4001,
        "server_pid": "auto_config_boot_server_pid"
      },
      "grpc_server": {
        "port": 50051
      },
      "reflectors": []
    },
    {
      "node_name": "node@master.com",
      "default_namespace": "UDPCanInterface",
      "chains": [
        {
          ...
        }
      ],
      "gateway": {
        "gateway_pid": "gateway_pid",
        "tcp_socket_port": 4042
      },
      "auto_config_boot_server": {
        "port": 4002,
        "server_pid": "auto_config_boot_server_pid"
      },
      "grpc_server": {
        "port": 50051
      },
      "reflectors": []
    }
  ]
}

```

## Trubleshoot

To start from a clean configuration you could do:
```bash
rm beamylabs-start/configuration/boot
```
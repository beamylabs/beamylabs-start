# Simple python example

## Setup
```bash
pip3 install grpcio requests protobuf
```

Example; from [here](simple_ecu/) run
```
python3 ecu.py --ip <ip_address>
```
for a more advanced example
```
python3 ecu_advanced.py --ip <ip_address>
```

To show available options/usage run script with -h 
```
python3 ecu.py -h
```

> **make sure that this line point to your installation https://github.com/beamylabs/beamylabs-start/blob/master/examples/grpc/python/simple_ecu/ecu.py#L100 (keep the port 50051)**

> this example works on any linux as it uses [udp](simple_ecu/configuration_udp) per default. If you like to use [can](simple_ecu/configuration) you need a can enabled device. Then enable this [line](https://github.com/beamylabs/beamylabs-start/blob/master/examples/grpc/python/simple_ecu/ecu.py#L107)

## Setup Windows
Download python 3.x from [here](https://www.python.org/downloads/) 

Follow the installer
> it's recommended to enable "Add python.exe to Path"

Run shell (terminal or powershell) as administrator, install necessary tools via pip
```
python -m pip instaLL grpcio-tools
python -m pip install grpcio-tools protobuf
```
Example; from [here](simple_ecu/) run
```
python3 ecu.py --ip <ip_address>
```
for a more advanced example
```
python3 ecu_advanced.py --ip <ip_address>
```

To show available options/usage run script with -h
```
python3 ecu.py -h
```

> **make sure that this line point to your installation https://github.com/beamylabs/beamylabs-start/blob/master/examples/grpc/python/simple_ecu/ecu.py#L142 (keep the port 50051)**


## Re-generate stubs

to re-generate files (already generated in the [common/generated](common/generated/) folder)

```bash
python -m grpc_tools.protoc -I../../../proto_files --python_out=./common/generated --grpc_python_out=./common/generated ../../../proto_files/*
```

## Configuration
Most of the python examples contains one or several configurations to try out. If you have a wish to create your own configuration, this section will cover what a configuration require to include and whats important when writing your own interface. 

A typical configuration includes a folder contaning dbc-files and an interface.json file. For reference, check out the configuration-examples [here](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python/simple_ecu).

### Interface
Open up a `interface.json` in one of the configuration-examples mentioned above to easier follow along.

Every interface starts with a ` "default_namespace"` , that namespace is required to exist in the `chains` for a correct interface. 
```json
"default_namespace": "VirtualInterface",
  "chains": [
    {
      "device_name": "virtual",
      "namespace": "VirtualInterface",
      "type": "virtual"
    },
    ...
```
Above you can see that the `"default_namespace"` is set to `"VirtualInterface"` and that namespace exists in the `"chains"`.


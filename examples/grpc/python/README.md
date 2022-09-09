# Simple python example

## Quick start

If you have `python3` installed jump ahead to [this guide](simple_ecu/README.md).

## Setup

```bash
pip3 install --upgrade pip
pip3 install grpcio requests protobuf
```

Example; from [here](simple_ecu/) run:

```bash
python3 ecu.py --url <address>
```

To show available options/usage run script with `-h`.

```bash
python3 ecu.py -h
```

> this example works on any linux as it uses [UDP](simple_ecu/configuration_udp) per default. If you like to use [CAN](simple_ecu/configuration_can) you need a can enabled device. Then enable [this line](https://github.com/beamylabs/beamylabs-start/blob/0fe6746c960b1612a4818f75789712f5f2b929be/examples/grpc/python/simple_ecu/ecu.py#L242)

## Setup Windows
Download python 3.x from [here](https://www.python.org/downloads/).

Follow the installer
> it's recommended to enable "Add python.exe to Path"

Run shell (terminal or Powershell) as administrator, install necessary tools via pip:

```bash
python3 -m pip install grpcio-tools
python3 -m pip install grpcio-tools protobuf
```
Example; from [here](simple_ecu/) run:

```
python3 ecu.py --ip <ip_address>
```

To show available options/usage run script with `-h`:

```bash
python3 ecu.py -h
```

> **Make sure to provide an ip that points to your installation when running the script OR change the ip in the code on [this line](https://github.com/beamylabs/beamylabs-start/blob/0fe6746c960b1612a4818f75789712f5f2b929be/examples/grpc/python/simple_ecu/ecu.py#L220) (keep the port 50051)**

## Re-generate stubs

to re-generate files (already generated in the [common/generated](common/generated/) folder)

```bash
python -m grpc_tools.protoc -I../../../proto_files --python_out=./common/generated --grpc_python_out=./common/generated ../../../proto_files/*
```

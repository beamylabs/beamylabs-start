# Simple python example

## Setup
```bash
pip3 install grpci requests
```

Example; from [here](simple_ecu/) run
```
python ecu.py
```
for a more advanced example
```
python ecu_advanced.py 
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
python ecy.py
```

> **make sure that this line point to your installation https://github.com/beamylabs/beamylabs-start/blob/master/examples/grpc/python/simple_ecu/ecu.py#L142 (keep the port 50051)**


## Re-generate stubs

to re-generate files (already generated in the [common/generated](common/generated/) folder)

```bash
python -m grpc_tools.protoc -I../../../proto_files --python_out=./common/generated --grpc_python_out=./common/generated ../../../proto_files/*
```

## Run
modify localhost in the sample code to the ip where your server is running.
run the simple_example.sh from your terminal.
```bash
python simple_example.sh
```

make sure you have can traffic running eg "cangen vcan0  -v -g 4" check root readme. Have patience.

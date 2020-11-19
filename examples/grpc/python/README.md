# Simple python example

## Setup
```bash
pip install grpcio-tools
```

Example; from [here](simple_ecu/) run
```
python ecy.py
```

> **make sure that this line point to your installation https://github.com/beamylabs/beamylabs-start/blob/master/examples/grpc/python/simple_ecu/ecu.py#L142 (keep the port 50051)**

## Setup Windows
use installer [here](https://www.python.org/downloads/release/python-2718/) donwload 2.7 version [link](https://www.python.org/ftp/python/2.7.18/python-2.7.18.msi)

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

to re-generate files (already generated in the [generated](generated/) folder)

```bash
python -m grpc_tools.protoc -I../../../proto_files --python_out=./generated --grpc_python_out=./generated ../../../proto_files/*
```

## Run
modify localhost in the sample code to the ip where your server is running.
run the simple_example.sh from your terminal.
```bash
python simple_example.sh
```

make sure you have can traffic running eg "cangen vcan0  -v -g 4" check root readme. Have patience.

# Example of virtual network: 
## Publisher and Subscriber
This examples uses both `virtual_example_pub.py` and `virtual_example_sub.py`.
By running them in separate terminals:
* You can use `virtual_example_pub.py` to type numbers in the console and send them to the SignalBroker using grpc.
* `virtual_example_sub.py` will subscribe to the SignalBroker and receive the stream of data. Every time you type a new number in the "Publisher" you will see the data received in the "Subscriber" side.

## Run
1. Make sure you have an `interfaces.json` file that contains `"type": "virtual"` in its `"chains"` array :
```json
    "chains": [
      {
        "device_name": "virtual",
        "namespace": "VirtualInterface",
        "type": "virtual"
      }
    ],
  ```
  > The `interfaces.json` file that you can find in the `config` folder already has this included.

2. Start the SignalBroker with this new configuration.
3. Execute `virtual_example_sub.py` on a new terminal.
4. In a different terminal, execute `virtual_example_pub.py`.
5. Write numbers in the terminal where you execute `virtual_example_pub.py`.
6. Watch those same numbers appear in the terminal where you execute `virtual_example_sub.py`

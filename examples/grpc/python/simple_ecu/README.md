# Simple ecu
Simple_ecu folder contains two scripts, **ecu.py** and **ecu_advanced.py**. With intention to give example and inspiration to further development. To get started and to get more details of the examples, continue reading.
## Pre-requisites
> If you haven't yet installed the necessary requirements to run python examples. Then we suggest you start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python#readme).

> Have knowledge of the ip address to your signal-broker installation

## Get started
### Options
The scripts ecu.py and ecu_advanced.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your signal-broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 ecu.py --ip 192.168.0.xxx`
* `-h` - Help, shows available options for script, run `python3 ecu.py -h`

### Default instructions
* Run shell (terminal, powershell, etc.).
* From [this folder](.) run
  * `python3 ecu.py --ip <ip_address>` or
  * `python3 ecu_advanced.py --ip <ip_address>` - for a more advanced example

### ecu.py

| Functions            | Description                                | Link  |
| -------------------- | ------------------------------------------ | ----- |
| read_signal          | Reads signals                              | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L29-L46) |
| publish_signals      | Publish signals                            | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L49-L73) |
| ecu_A                | Publishes value, read other value          | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L76-L113) |
| ecu_B_read           | Read value published by ecu_A              | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L116-L138) |
| ecu_B_subscribe      | Subscribe to value published by ecu_A      | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L141-L178) |
| read_on_timer        | Reads signals with timer                   | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L181-L207) |
| run                  | Main function                              | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu.py#L210-L280) |


### ecu_advanced.py

| Functions            | Description                                | Link  |
| -------------------- | ------------------------------------------ | ----- |
| read_signal          | Reads signals                              | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L29-L46) |
| publish_signals      | Publish signals                            | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L49-L70) |
| ecu_A                | Publishes value, read other value          | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L76-L136) |
| ecu_B_read           | Read value published by ecu_A              | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L139-L161) |
| ecu_B_subscribe      | Subscribe to value published by ecu_A      | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L164-L199) |
| ecu_B_subscribe_2    | Variant of above function, shows potential | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L202-L253) |
| read_on_timer        | Reads signals with timer                   | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L256-L282) |
| run                  | Main function                              | [ref](https://github.com/beamylabs/beamylabs-start/blob/8872658077838f67f5c035929f6429afc3b81bbd/examples/grpc/python/simple_ecu/ecu_advanced.py#L285-L376) |


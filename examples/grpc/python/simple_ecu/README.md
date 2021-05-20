# Simple ecu
This contains example of 
## Pre-requisites
* If you haven't yet installed the necessary requirements to run python examples. Start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python#readme).
* ip address to your installation

## Get started
The example scripts in this folder (ecu.py and ecu_advanced.py) can be started with options `-h` or `--ip <ip_address>`.

### Options
* `--ip <ip_address>` - Points to the ip of your signal-broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 ecu.py --ip 192.168.0.000`
`-h` - Help, shows available options for script, run `python3 ecu.py -h`

### Default instructions
* Run shell (terminal, powershell, etc.).
* From [here](simple_ecu/) run
⋅⋅* `python3 ecu.py --ip <ip_address>`
⋅⋅* `python3 ecu_advanced.py --ip <ip_address>` - for a more advanced example

#### ecu.py

| Functions            | Description                                | Link  |
| -------------------- | ------------------------------------------ | ----- |
| read_signal          | Reads signals                              | [ref] |
| publish_signals      | Publish signals                            | [ref] |
| ecu_A                | Publishes value, read other value          | [ref] |
| ecu_B_read           | Read value published by ecu_A              | [ref] |
| ecu_B_subscribe      | Subscribe to value published by ecu_A      | [ref] |
| read_on_timer        | Reads signals with timer                   | [ref] |
| run                  | Main function                              | [ref] |


#### ecu_advanced.py

| Functions            | Description                                | Link  |
| -------------------- | ------------------------------------------ | ----- |
| read_signal          | Reads signals                              | [ref] |
| publish_signals      | Publish signals                            | [ref] |
| ecu_A                | Publishes value, read other value          | [ref] |
| ecu_B_read           | Read value published by ecu_A              | [ref] |
| ecu_B_subscribe      | Subscribe to value published by ecu_A      | [ref] |
| ecu_B_subscribe_2    | Variant of above function, shows potential | [ref] |
| read_on_timer        | Reads signals with timer                   | [ref] |
| run                  | Main function                              | [ref] |


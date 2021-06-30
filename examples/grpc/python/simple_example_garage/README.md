# Simple example garage
Simple_example_garage folder contains one script, **simple_example_garage.py**. With intention to give example and inspiration to further development. To get started and to get more details of the example, continue reading.

## Pre-requisites
> If you haven't yet installed the necessary requirements to run python examples. Then we suggest you start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python#readme).

> Have knowledge of the ip address to your beamy broker installation, if you have the web-client running you can get the ip in the bottom left corner.

## Get started
### Options
The scripts simple_example_garage.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your beamy broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 simple_example_garage.py --ip 192.168.xxx.xxx`
* `-h` - Help, shows available options for script, run `python3 resp_to_diag_req.py -h`

### Default instructions
* Run shell (terminal, powershell, etc.).
* From [this folder](.) run
  * `python3 simple_example_garage.py --ip <ip_address>`

### Overview
This is an example script and it all starts in the main function `def run(argv):`. Lets break it down.

#### Setting up stubs and configuration
First we start of with setting up a connection to the beamy broker (with the ip that was passed to the script) and then defining the grpc stubs that will be used. In code it looks like this:
```
channel = grpc.insecure_channel(ip + port)
network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
diag_stub = diagnostics_api_pb2_grpc.DiagnosticsServiceStub(channel)
system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
functional_stub = functional_api_pb2_grpc.FunctionalServiceStub(channel)
```

#### Configuration
Simple_example_garage folder contains a sample configuration, [configuration](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python/simple_example_garage/configuration). The script uploads and reloads configuration with the `system_stub` that was defined above.
It will look like this:
```
upload_folder(system_stub, "configuration")
reload_configuration(system_stub)
```

#### Functions
After all is set up the script includes various functions to use, some of them are commented out in the code but feel free to uncomment. Here is a list of available functions:

* subscribe_to_fan_speed - Subscribes to fan speed
* read_diagnostics_vin - Read diagnostics
* read_diagnostics_odb - Read diagnostics
* subscribe_to_arbitration - Subscribe to LIN arbitration
* publish_signals - Publish signals only once
* set_fan_speed - Sets fan speed

#### Support
If you have any further questions, please reach out! 

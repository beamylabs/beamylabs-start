# Resp to diag
Resp_to_diag folder contains one script, **resp_to_diag_req.py**. The script can subscribe to one or multiple signals and/or publish signal. This with intention to give example and inspiration to further development. To get started and to get more details of the example, continue reading.
## Pre-requisites
> If you haven't yet installed the necessary requirements to run python examples. Then we suggest you start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python#readme).

> Have knowledge of the ip address to your beamy broker installation, if you have the web-client running you can get the ip in the bottom left corner.

## Get started
### Options
The scripts resp_to_diag_req.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your beamy broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 resp_to_diag_req.py --ip 192.168.xxx.xxx`
* `-h` - Help, shows available options for script, run `python3 resp_to_diag_req.py -h`

### Default instructions
* Run shell (terminal, powershell, etc.).
* From [this folder](.) run
  * `python3 resp_to_diag_req.py --ip <ip_address>`

### Overview
This is a simple example and it all starts in the main function `def run(argv):`. Lets break it down.

#### Setting up stubs and configuration
First we start of with setting up a connection to the beamy broker (with the ip that was passed to the script) and then defining the grpc stubs that will be used. In code it looks like this:
```
  channel = grpc.insecure_channel(ip + port)
  network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
  system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
  client_id = common_pb2.ClientId(id="app_identifier")
```

#### Configuration
Resp_to_diag folder contains a sample configuration, [configuration](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python/resp_to_diag/configuration). The script uploads and reloads configuration with the `system_stub` that was defined above.
It will look similar to this:
```
upload_folder(system_stub, "configuration")
reload_configuration(system_stub)
```

#### Define and Subscribe 
First off we need to define som signals/frames to subscribe to. We create a SignalId that requires a name and a namespace. In the code it exists some examples of how to define them and it looks like this:
```
diag_frame_req = common_pb2.SignalId(
  name="DiagReqFrame_2016",
  namespace=common_pb2.NameSpace(name="DiagnosticsCanInterface"),
)
diag_frame_resp = signal = common_pb2.SignalId(
  name="DiagResFrame_2024",
  namespace=common_pb2.NameSpace(name="DiagnosticsCanInterface"),
)
```
Then all we have to do is pass them to the function call `subscribe_to_diag` along with a `client_id` and the `network_stub`.
```
subscribe_to_diag(client_id, network_stub, diag_frame_req, diag_frame_resp)
```

The script also includes a function for publishing a signal - `publish_signals` - which takes one SignalId, besides client_id and the network stub.

#### Support
If you have any further questions, please reach out! 
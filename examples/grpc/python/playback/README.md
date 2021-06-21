# Playback
Playback folder contains one script, **playback.py**. The script can start one or multiple playbacks and holds various functions to listen and/or subscribe to signals. This with intention to give example and inspiration to further development. To get started and to get more details of the examples, continue reading.

## Pre-requisites
> If you haven't yet installed the necessary requirements to run python examples. Then we suggest you start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python#readme).

> Have knowledge of the ip address to your beamy broker installation, if you have the web-client running you can get the ip in the bottom left corner.

## Get started
### Options
The script playback.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your beamy broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 playback.py --ip 192.168.xxx.xxx`
* `-h` - Help, shows available options for script, run `python3 playback.py -h`

 ### Default instructions
* Run shell (terminal, powershell, etc.).
* From [this folder](.) run
  * `python3 playback.py --ip <ip_address>`

### Overview
A bunch of things are going on in this examples and it all starts in the main function `def run(argv):`. Lets break it down.

#### Setting up stubs and configuration
First we start of with setting up a connection to the beamy broker (with the ip that was passed to the script) and then defining the grpc stubs that will be used. In code it looks like this:
```
  channel = grpc.insecure_channel(ip + port)
  network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
  traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
  system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
  check_license(system_stub)
```

#### Configuration
Playback folder contains a sample configuration, [configuration_custom_udp](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python/playback/configuration_custom_udp). The playback script uploads and reloads configuration with the `system_stub` that was defined above. Feel free to use your own.
It will look similar to this:
```
upload_folder(system_stub, "configuration_custom_udp")
reload_configuration(system_stub)
```

#### Upload recording
The file you want to do a playback on first needs to be uploaded.
In the script you have this part: 
```
upload_file(
  system_stub,
  "recordings/traffic.log",
  "recordings/candump_uploaded.log",
)
```
It uploads the file with the `system_stub`, second argument points to the filepath of your file (in the playback folder it exists a sample file `recordings/traffic.log`) and third argument, the path and name of the uploaded file.

#### Playback
Next part of the script creates a list, this list can contain one or several playbacksettings. Each playbacksetting needs to have a `namespace`, a `path` and a `mode`. The script continues with starting all playbacks in the list. In code it look like this:
```
playbacklist = [
  {
    "namespace": "custom_can",
    "path": "recordings/candump_uploaded.log",
    "mode": traffic_api_pb2.Mode.PLAY,
  }
]
# Starts playback
status = traffic_stub.PlayTraffic(
  traffic_api_pb2.PlaybackInfos(
    playbackInfo=list(map(create_playback_config, playbacklist))
  )
)
```

> If changing the playbacklist, also copy and replace the playbacklist in function `stop_playback`, for a nice and clean exit of the script.

#### Support
More details about the Threads in the script; `read_signal`, `ecu_B_read`, `ecu_B_subscribe` or  `read_on_timer`, can be read [here](https://github.com/beamylabs/beamylabs-start/blob/master/examples/grpc/python/simple_ecu/README.md).
If you have any further questions, please reach out! 

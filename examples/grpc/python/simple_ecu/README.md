# Simple ecu
Simple_ecu folder contains two scripts, **ecu.py** and **ecu_advanced.py**. With intention to give example and inspiration to further development. To get started and to get more details of the examples, continue reading.
## Pre-requisites
> If you haven't yet installed the necessary requirements to run python examples. Then we suggest you start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python#readme).

> Have knowledge of the ip address to your beamy broker installation, if you have the web-client running you can get the ip in the bottom left corner.

## Get started
### Options
The scripts ecu.py and ecu_advanced.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your beamy broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 ecu.py --ip 192.168.0.xxx`
* `-h` - Help, shows available options for script, run `python3 ecu.py -h`

### Default instructions
* Run shell (terminal, powershell, etc.).
* From [this folder](.) run
  * `python3 ecu.py --ip <ip_address>` or
  * `python3 ecu_advanced.py --ip <ip_address>` - for a more advanced example

### Overview
A bunch of things are going on in this examples and it all starts in the main function `def run(argv):`. Lets break it down.

#### Setting up stubs and configuration
First we start of with setting up a connection to the beamy broker (with the ip that was passed to the script) and then defining the grpc stubs that will be used. In code it looks like this:
```
  channel = grpc.insecure_channel(ip + port)
  network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
  system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
  check_license(system_stub)
```

#### Configuration
Simple ecu folder contains some examples of different configurations, available configurations to use are the following:
* [configuration](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python/simple_ecu/configuration)
* [configuration_can](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python/simple_ecu/configuration_can)
* [configuration_lin](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python/simple_ecu/configuration_lin)
* [configuration_udp](https://github.com/beamylabs/beamylabs-start/tree/improve-sample-and-docs/examples/grpc/python/simple_ecu/configuration_udp)

The example scripts uploads and reloads configuration with the `system_stub` that was defined above. Some lines are commented and not in use, but you can easily uncomment a line to shift between configurations or feel free to use your own.
It will look similar to this:
```
# upload_folder(system_stub, "configuration")
upload_folder(system_stub, "configuration_udp")
# upload_folder(system_stub, "configuration_lin")
# upload_folder(system_stub, "configuration_can")
reload_configuration(system_stub)
```

#### Threads
The last part of the example scripts are starting up threads, you can read the docs for threading [here](https://docs.python.org/3/library/threading.html). 
In both examples you will see a thread called `ecu_A_thread`, this thread defines the target-function `ecu_A` and will then start the thread. 
```
ecu_A_thread = Thread(
  target=ecu_A,
  args=(
    network_stub,
    1,
  ),
)
ecu_A_thread.start()
```
The function `ecu_A` will publish one or multiple signals which then can be caught and read by ecu_B. In this examples `ecu_A` also reads a value that's been published by ecu_B.

Next up we see a thread called `ecu_B_threads` which shows how to read signals that has been published on ecu_A. The thread `read_on_timer` is a variant of this and also has the purpose to read.

Last but not least we have the thread `ecu_B_thread_subscribe`, this thread uses target-function `ecu_B_subscribe`. This function will first subscribe to a value, 'counter'. 
```
counter = common_pb2.SignalId(
  name="counter", namespace=common_pb2.NameSpace(name=namespace)
)
sub_info = network_api_pb2.SubscriberConfig(
  clientId=client_id,
  signals=network_api_pb2.SignalIds(signalId=[counter]),
  onChange=True,
)
```
Then every time the `counter` signal comes, the function will take the value from the incoming signal, double the value and publish it as another signal `counter_times_2` (which then can be read by ecu_A). I will look like this:
```
try:
  for subs_counter in stub.SubscribeToSignals(sub_info):
    for signal in subs_counter.signal:
      print("ecu_B, (subscribe) counter is ", signal.integer)
      counter_times_2 = common_pb2.SignalId(
        name="counter_times_2",
        namespace=common_pb2.NameSpace(name=namespace),
      )
      signal_with_payload = network_api_pb2.Signal(
        id=counter_times_2, integer=signal.integer * 2
      )
      publish_signals(client_id, stub, [signal_with_payload])

except grpc._channel._Rendezvous as err:
  print(err)
```
The script `ecu_advanced.py` has a second subscribe function, with the main purpose to show that it's possible to subscribe multiple times to the same signal but also to show a variant on how to subscribe to multiple signals at once.

#### Support
If you have any further questions, please reach out! 
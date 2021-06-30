# Example of virtual network
A virtual network allows devices (or client programs) connected to the server to exchanges massages (over ip). The client programs can reside on any harware and be implemented in any programming language.

> typical scenario could by some code snippet (client program) used to toggle some relays, which is controlled from another snippet.
> Currently there is no support of listing signals in virtual networks.

## Pre-requisites
> If you haven't yet installed the necessary requirements to run python examples. Then we suggest you start by following instructions [here](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python#readme).

> Have knowledge of the ip address to your beamy broker installation, if you have the web-client running you can get the ip in the bottom left corner.

## Get started
### Options
The scripts virtual_example_pub.py and virtual_example_sub.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your beamy broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing: `python3 virtual_example_pub.py --ip 192.168.xxx.xxx`
* `-h` - Help, shows available options for script, run `python3 virtual_example_pub.py -h`

### Default instructions
* Run a new shell (terminal, powershell, etc.).
* From [this folder](.) execute:
  * `python3 virtual_example_sub.py --ip <ip_address>`
  * This will also upload relevant configuration
* In a different shell execute:
  * `python3 virtual_example_pub.py.py --ip <ip_address>`
  * Write numbers in this terminal
* Watch those same numbers appear in the terminal where you executed `virtual_example_sub.py`

### Overview
A bunch of things are going on in this examples and it all starts in the main function `def run(argv):`. Lets break it down.

#### Setting up stubs and configuration
First we start of with setting up a connection to the beamy broker (with the ip that was passed to the script) and then defining a channel and the grpc stubs that will be used. In code it looks similar to this:
```
channel = grpc.insecure_channel(ip + port)
network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
```
Virtual_example_sub.py also checks license, uploads configuration and reloads configuration. 
```
system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
check_license(system_stub)
upload_folder(system_stub, "configuration")
reload_configuration(system_stub)
```

#### Publisher and Subscriber
This examples uses both `virtual_example_pub.py` and `virtual_example_sub.py`.
By running them in separate terminals:
* You can use `virtual_example_pub.py` to type numbers in the console and send them to the SignalBroker using grpc.
* `virtual_example_sub.py` will subscribe to the SignalBroker and receive the stream of data. Every time you type a new number in the "Publisher" you will see the data received in the "Subscriber" side.

##### Details: virtual_example_sub.py
This script creates a signal to subscribe on, a configuration for the subscription and then tries to subscribe to that signal. In code it looks like this:
```
# Create a signal
namespace = common_pb2.NameSpace(name="VirtualInterface")
signal = common_pb2.SignalId(name="virtual_signal", namespace=namespace)

# Create a subscriber config
client_id = common_pb2.ClientId(id="virtual_example_sub")
signals = network_api_pb2.SignalIds(signalId=[signal])
sub_info = network_api_pb2.SubscriberConfig(
  clientId=client_id, signals=signals, onChange=False
)

# Subscribe
try:
  for response in network_stub.SubscribeToSignals(sub_info):
    print(response)
  except grpc._channel._Rendezvous as err:
    print(err)
```

##### Details: virtual_example_pub.py
This script takes an input value (number). Then it creates a signal to publish, a configuration and then tries to publish that signal. It is this part of the code:
```
# Create a signal
namespace = common_pb2.NameSpace(name="VirtualInterface")
signal = common_pb2.SignalId(name="virtual_signal", namespace=namespace)

# Add payload to the signal
signal_with_payload = network_api_pb2.Signal(id=signal)
signal_with_payload.integer = signal_value

# Create a publisher config
client_id = common_pb2.ClientId(id="virtual_example_pub")
signals = network_api_pb2.Signals(signal=(signal_with_payload,))
publisher_info = network_api_pb2.PublisherConfig(
  clientId=client_id, signals=signals, frequency=0
)

# Publish
  try:
      network_stub.PublishSignals(publisher_info)
  except grpc._channel._Rendezvous as err:
    print(err)
```

#### Support
If you have any further questions, please reach out! 

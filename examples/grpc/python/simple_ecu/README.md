# Simple ecu
Simple_ecu folder contains **ecu.py**. With intention to give example and inspiration to further development. To get started and to get more details of the examples, continue reading.

Simple ecu simulates 2 ecu:s which are connected (using `LIN`/`CAN`/`udp`) (defaults to `upd`)
> If you use `CAN` devices you need to connect the connectors, creating you own simple network (remember to terminated the ends).

`Ecu_A`:
- Publishes `counter` signal on a timer.  
- Synchronously reads `counter_times_2` and prints the results.

`Ecu_B`:
- Subscribes to `counter`
- Doubles the value and publishes `counter_times_2` 
> Ecu_B also showcases a syncronous read using a timer.

## Pre-requisites

> Have knowledge of the ip address to your beamy broker installation, if you have the web-client running you can get the ip in the bottom left corner.

## Get started

from *this* location run:
```
pip install -r requirements.txt
```

> if you don't have python3 installed go [here](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python#readme) 
### Options

ecu.py can be started with options `-h` or `--ip <ip_address>`.
* `--ip <ip_address>` - Points to the ip of your beamy broker installation, if this option is not used the scripts will use ip `127.0.0.1`. For example start the script by typing:
`python3 ecu.py --ip 192.168.0.xxx`

* `-h` - Help, shows available options for script, run `python3 ecu.py -h`

### Default instructions
* Run shell (terminal, powershell, etc.).
* From [this folder](.) run
  * `python3 ecu.py --ip <ip_address>`

### Overview
A bunch of things are going on in this examples and it all starts in the main function `def run(argv):`. Lets break it down.

#### Setting up stubs and configuration
First we start of with setting up a connection to the beamy broker (with the ip that was passed to the script) and then defining the grpc stubs that will be used. In code it looks like this:
```pyhton
  channel = grpc.insecure_channel(ip + port)
  network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
  system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
  check_license(system_stub)
```

#### Configuration
Simple ecu folder contains some examples of different configurations, available configurations to use are the following:
* [configuration_can](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python/simple_ecu/configuration_can)
* [configuration_lin](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python/simple_ecu/configuration_lin)
* [configuration_udp](https://github.com/beamylabs/beamylabs-start/tree/master/examples/grpc/python/simple_ecu/configuration_udp)

The example scripts uploads and reloads configuration with the `system_stub` that was defined above. Some lines are commented and not in use, but you can easily uncomment a line to shift between configurations or feel free to use your own.
It will look similar to this:
```
upload_folder(system_stub, "configuration_udp")
# upload_folder(system_stub, "configuration_lin")
# upload_folder(system_stub, "configuration_can")
reload_configuration(system_stub)
```
> For `CAN`/`LIN` to work you need seperate HW.
#### Threads
The last part of `ecu.py` is starting up threads, you can read the docs for threading [here](https://docs.python.org/3/library/threading.html). 
You will see a thread called `ecu_A_thread`, this thread defines the target-function `ecu_A` and will then start the thread. 
```python
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

Next up we see a thread called `ecu_B_sub_thread` which shows how to subscribe to signals that has been published by ecu_A. The thread `ecu_read_on_timer` is a synchronous variant of this and also has the purpose to read.

`ecu_B_sub_thread` thread uses `act_on_signal` which will invoke provided function (here a lambda) once a subscrpition is triggered on any of the provided signals.
```python
for subs_counter in subscripton:
    fun(subs_counter.signal)
```

```python
ecu_B_sub_thread = Thread(
    target=act_on_signal,
    args=(
        ecu_b_client_id,
        network_stub,
        [
            signal_creator.signal("counter", "ecu_B"),
        ],
        True,  # only report when signal changes
        lambda signals: double_and_publish(
            network_stub,
            ecu_b_client_id,
            signal_creator.signal("counter", "ecu_B"),
            signals,
        ),
    ),
)
```

Every time the `counter` signal comes, the function will take the value from the incoming signal, double the value and publish it as another signal `counter_times_2` (which then can be read by ecu_A). I will look like this:
```python
def double_and_publish(network_stub, client_id, trigger, signals):
    for signal in signals:
        print(f"ecu_B, (subscribe) {signal.id.name} {get_value(signal)}")
        if signal.id == trigger:
            publish_signals(
                client_id,
                network_stub,
                [
                    signal_creator.signal_with_payload(
                        "counter_times_2", "ecu_B", ("integer", get_value(signal) * 2)
                    ),
                ],
            )
```

#### Support
If you have any further questions, please reach out! 

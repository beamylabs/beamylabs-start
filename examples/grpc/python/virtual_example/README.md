# Example of virtual network
A virtual network allows devices (or client programs) connected to the server to exchanges massages (over ip). The client programs can reside on any harware and be implemented in any programming language.

> typical scenario could by some code snippet (client program) used to toggle some relays, which is controlled from another snippet.
> Currently there is no support of listing signals in virtual networks.

## Publisher and Subscriber
This examples uses both `virtual_example_pub.py` and `virtual_example_sub.py`.
By running them in separate terminals:
* You can use `virtual_example_pub.py` to type numbers in the console and send them to the SignalBroker using grpc.
* `virtual_example_sub.py` will subscribe to the SignalBroker and receive the stream of data. Every time you type a new number in the "Publisher" you will see the data received in the "Subscriber" side.

## Run
1. Execute `virtual_example_sub.py` on a new terminal. This will also upload the relevant configuration
2. In a different terminal, execute `virtual_example_pub.py`.
3. Write numbers in the terminal where you execute `virtual_example_pub.py`.
4. Watch those same numbers appear in the terminal where you execute `virtual_example_sub.py`
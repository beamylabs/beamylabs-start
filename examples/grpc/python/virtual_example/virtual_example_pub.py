#!/usr/bin/env python3
# Copyright 2015 gRPC authors.
# Copyright 2019 Volvo Cars
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This examples shows how to publish signals to the virtual interface in SignalBroker.

This example works with 'virtual_example_sub.py' and it is meant to receive the signals publish from here.
In this code we get user input from the console (only 10 times then we stop).
Each time we capture a number, we publish it as the value of signal called 'virtual_signal' in the 'virtual' namespace.
Note that there is no need to specify a database for this kind of signals.

"""
import grpc

import sys, getopt

sys.path.append("../common/generated")

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2

sys.path.append("../common")
import helper
from helper import *

__author__ = "Aleksandar Filipov and Alvaro Alonso"
__copyright__ = "Copyright 2019, Volvo Cars Group"

__version__ = "0.0.1"
__maintainer__ = "Alvaro Alonso"
__email__ = "aalonso@volvocars.com"
__status__ = "Development"


def run(argv):
    """Main function, checking arguments passed to script, setting up stub and publishes signals with user input.

    Parameters
    ----------
    argv : list
        Arguments passed when starting script

    """
    # Checks argument passed to script, virtual_example_pub.py will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1"
    # Keep this port
    port = ":50051"
    try:
        opts, args = getopt.getopt(argv, "h", ["ip="])
    except getopt.GetoptError:
        print("Usage: virtual_example_pub.py --ip <ip_address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: virtual_example_pub.py --ip <ip_address>")
            sys.exit(2)
        elif opt == "--ip":
            ip = arg

    # Create a channel
    channel = grpc.insecure_channel(ip + port)
    # Create the stub
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    # For 10 messages
    for _ in range(10):
        input_value = input("Enter a number: ")
        try:
            signal_value = int(input_value)
        except ValueError:
            print(f"{input_value} is not a number. Only numbers are allowed")
        else:
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

if __name__ == "__main__":
    run(sys.argv[1:])
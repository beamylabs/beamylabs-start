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

import sys
import binascii

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


if __name__ == "__main__":
    # Create a channel
    channel = grpc.insecure_channel("localhost:50051")
    # Create the stub
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)
    upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)
    # create the identifier of *this* client
    client_id = common_pb2.ClientId(id="virtual_example_pub")
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
            signal = common_pb2.SignalId(name="my_madeup_virtual_signal", namespace=namespace)
            # Add payload to the signal
            signal_with_payload = network_api_pb2.Signal(id=signal)
            # 20 bytes chosen as an arbitrary number
            signal_with_payload.raw = signal_value.to_bytes(20, 'big')
            # long vectors are valid on virtual networks!
            # signal_with_payload.integer = signal_value
            # Create a publisher config
            signals = network_api_pb2.Signals(signal=(signal_with_payload,))
            publisher_info = network_api_pb2.PublisherConfig(
                clientId=client_id, signals=signals, frequency=0
            )
            # Publish
            try:
                network_stub.PublishSignals(publisher_info)
            except grpc._channel._Rendezvous as err:
                print(err)

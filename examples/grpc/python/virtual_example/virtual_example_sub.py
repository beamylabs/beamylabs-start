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

"""This examples shows how to subscribe to a virtual signal in a virtual interface of SignalBroker

This example works with 'virtual_example_pub.py' and it is meant to receive the signals publish from 'virtual_example_pub.py'.
In this code we get the stream of data from the SignalBroker grpc server for the signal: ' input from the console (only 10 times then we stop).
Each time we capture a number we publish it as the value of signal 'virtual_signal' in the 'virtual' namespace.

"""
import grpc
import binascii
import sys

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

def get_value(signal):
    if signal.raw != b"":
        return "0x" + binascii.hexlify(signal.raw).decode("ascii")
    elif signal.HasField("integer"):
        return signal.integer
    elif signal.HasField("double"):
        return signal.double
    elif signal.HasField("arbitration"):
        return signal.arbitration
    else:
        return "empty"


if __name__ == "__main__":
    # Create a channel
    channel = grpc.insecure_channel("localhost:50051")
    # Create the system stup, to upload relevant confiuration
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)
    upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)
    # create the identifier of *this* client
    client_id = common_pb2.ClientId(id="virtual_example_sub")
    # Create the stub
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    # Create a signal
    namespace = common_pb2.NameSpace(name="VirtualInterface")
    signal = common_pb2.SignalId(name="my_madeup_virtual_signal", namespace=namespace)
    # Create a subscriber config
    signals = network_api_pb2.SignalIds(signalId=[signal])
    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id, signals=signals, onChange=False
    )
    # Subscribe
    while True:
        try:
            for response in network_stub.SubscribeToSignals(sub_info, timeout=None):
                for signal in response.signal:
                    print(f"received {signal.id.name} value is {get_value(signal)}")

        except grpc._channel._Rendezvous as err:
            print(err)

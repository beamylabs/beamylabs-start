#inspired by https://grpc.io/docs/tutorials/basic/python.html

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

"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import random
import time

import grpc

import sys
sys.path.append('generated')

import network_api_pb2
import network_api_pb2_grpc
import functional_api_pb2
import functional_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import diagnostics_api_pb2_grpc
import diagnostics_api_pb2


def subscribe_to_signal(stub):
    source = common_pb2.ClientId(id="app_identifier")
    signal = common_pb2.SignalId(name="SteerWhlAgSafe", namespace=common_pb2.NameSpace(name = "ChassisCANhs"))
    sub_info = network_api_pb2.SubscriberConfig(clientId=source, signals=network_api_pb2.SignalIds(signalId=[signal]), onChange=False)
    try:
        for response in stub.SubscribeToSignals(sub_info):
            print(response)
    except grpc._channel._Rendezvous as err:
            print(err)

import binascii


def run():
    channel = grpc.insecure_channel('localhost:50051')
    functional_stub = functional_api_pb2_grpc.FunctionalServiceStub(channel)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    diag_stub = diagnostics_api_pb2_grpc.DiagnosticsServiceStub(channel)

    print("-------------- Subscribe to signal blocking --------------")
    subscribe_to_signal(network_stub)


if __name__ == '__main__':
    run()

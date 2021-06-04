#!/usr/bin/env python2
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

import os
import random
import time

import grpc

import sys

sys.path.append("generated")

import network_api_pb2
import network_api_pb2_grpc
import functional_api_pb2
import functional_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import diagnostics_api_pb2_grpc
import diagnostics_api_pb2


def set_fan_speed(stub, value, freq):
    source_g = common_pb2.ClientId(id="app_identifier")
    value_g = functional_api_pb2.Value(payload=value)
    response = stub.SetFanSpeed(
        functional_api_pb2.SenderInfo(clientId=source_g, value=value_g, frequency=freq)
    )
    print("executed call %s" % response)


# make sure you have VirtualCanInterface namespace in interfaces.json
def subscribe_to_fan_signal(stub):
    source = common_pb2.ClientId(id="app_identifier")
    namespace = common_pb2.NameSpace(name="VirtualCanInterface")
    signal = common_pb2.SignalId(name="BenchC_c_2", namespace=namespace)
    sub_info = network_api_pb2.SubscriberConfig(
        clientId=source,
        signals=network_api_pb2.SignalIds(signalId=[signal]),
        onChange=False,
    )
    try:
        for response in stub.SubscribeToSignals(sub_info):
            print(response)
    except grpc._channel._Rendezvous as err:
        print(err)


import binascii


# https://en.wikipedia.org/wiki/OBD-II_PIDs
# Make sure to reference the diagnostics.dbc in your interfaces.json (which is already refrenced)
def read_diagnostics_odb(stub):
    source = common_pb2.ClientId(id="app_identifier")
    namespace = common_pb2.NameSpace(name="DiagnosticsCanInterface")
    upLink = common_pb2.SignalId(name="DiagReqBroadCastFrame_2015", namespace=namespace)
    # if you dont see any response try the other resp frames defined in the diagnostics dbc file.
    downLink = common_pb2.SignalId(name="DiagResFrame_2024", namespace=namespace)
    # service 01 pid 12 - engine rpm
    request = diagnostics_api_pb2.DiagnosticsRequest(
        upLink=upLink, downLink=downLink, serviceId=b"\x01", dataIdentifier=b"\x12"
    )
    try:
        response = stub.SendDiagnosticsQuery(request)
        print(response)
        print(binascii.hexlify(response.raw))
    except grpc._channel._Rendezvous as err:
        print(err)


def read_diagnostics_vin(stub):
    source = common_pb2.ClientId(id="app_identifier")
    namespace = common_pb2.NameSpace(name="ChassisCANhs")
    upLink = common_pb2.SignalId(
        name="VddmToAllFuncChasDiagReqFrame", namespace=namespace
    )
    downLink = common_pb2.SignalId(
        name="PscmToVddmChasDiagResFrame", namespace=namespace
    )

    request = diagnostics_api_pb2.DiagnosticsRequest(
        upLink=upLink, downLink=downLink, serviceId=b"\x22", dataIdentifier=b"\xF1\x90"
    )
    try:
        response = stub.SendDiagnosticsQuery(request)
        print(response)
        print(binascii.hexlify(response.raw))
    except grpc._channel._Rendezvous as err:
        print(err)


# make sure you have VirtualCanInterface namespace in interfaces.json
def subscribe_to_arbitration(stub):
    source = common_pb2.ClientId(id="app_identifier")
    namespace = common_pb2.NameSpace(name="VirtualCanInterface")
    signal = common_pb2.SignalId(name="BenchC_c_5", namespace=namespace)
    sub_info = network_api_pb2.SubscriberConfig(
        clientId=source,
        signals=network_api_pb2.SignalIds(signalId=[signal]),
        onChange=False,
    )
    try:
        for response in stub.SubscribeToSignals(sub_info):
            print(response)
    except grpc._channel._Rendezvous as err:
        print(err)


# make sure you have VirtualCanInterface namespace in interfaces.json
def publish_signals(stub):
    source = common_pb2.ClientId(id="app_identifier")
    namespace = common_pb2.NameSpace(name="VirtualCanInterface")

    signal = common_pb2.SignalId(name="BenchC_c_5", namespace=namespace)
    signal_with_payload = network_api_pb2.Signal(id=signal)
    signal_with_payload.integer = 4

    signal2 = common_pb2.SignalId(name="BenchC_c_2", namespace=namespace)
    signal_with_payload_2 = network_api_pb2.Signal(id=signal2)
    signal_with_payload_2.double = 3.4

    signal3 = common_pb2.SignalId(name="BenchC_d_2", namespace=namespace)
    signal_with_payload_3 = network_api_pb2.Signal(id=signal3)
    signal_with_payload_3.arbitration = True

    publisher_info = network_api_pb2.PublisherConfig(
        clientId=source,
        signals=network_api_pb2.Signals(
            signal=[signal_with_payload, signal_with_payload_2]
        ),
        frequency=0,
    )
    try:
        stub.PublishSignals(publisher_info)
        time.sleep(1)
    except grpc._channel._Rendezvous as err:
        print(err)


##################### START BOILERPLATE ####################################################

import hashlib
import posixpath
import ntpath


def get_sha256(file):
    f = open(file, "rb")
    bytes = f.read()  # read entire file as bytes
    readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash


# 20000 as in infinity
def generate_data(file, dest_path, chunk_size, sha256):
    for x in range(0, 20000):
        if x == 0:
            fileDescription = system_api_pb2.FileDescription(
                sha256=sha256, path=dest_path
            )
            yield system_api_pb2.FileUploadRequest(fileDescription=fileDescription)
        else:
            buf = file.read(chunk_size)
            if not buf:
                break
            yield system_api_pb2.FileUploadRequest(chunk=buf)


def upload_file(stub, path, dest_path):
    sha256 = get_sha256(path)
    print(sha256)
    file = open(path, "rb")

    # make sure path is unix style (necessary for windows, and does no harm om linux)
    upload_iterator = generate_data(
        file, dest_path.replace(ntpath.sep, posixpath.sep), 1000000, sha256
    )
    response = stub.UploadFile(upload_iterator)
    print("uploaded", path, response)


from glob import glob


def upload_folder(system_stub, folder):
    files = [
        y
        for x in os.walk(folder)
        for y in glob(os.path.join(x[0], "*"))
        if not os.path.isdir(y)
    ]
    for file in files:
        upload_file(system_stub, file, file.replace(folder, ""))


def reload_configuration(system_stub):
    request = common_pb2.Empty()
    response = system_stub.ReloadConfiguration(request, timeout=60000)
    print(response)


##################### END BOILERPLATE ####################################################


def run():
    #     channel = grpc.insecure_channel('192.168.1.82:50051')
    channel = grpc.insecure_channel("192.168.1.184:50051")
    functional_stub = functional_api_pb2_grpc.FunctionalServiceStub(channel)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    diag_stub = diagnostics_api_pb2_grpc.DiagnosticsServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)

    #     print("-------------- Subsribe to fan speed BLOCKING --------------")
    #     subscribe_to_fan_signal(network_stub)

    print("-------------- upload folder and reload--------------")
    #     upload_folder(system_stub, "../../../../configurations/demo-torslanda")
    #     upload_folder(system_stub, "../../../../configurations/mountainview")
    upload_folder(system_stub, "../../../../configurations/vanilla-osx")
    reload_configuration(system_stub)

    # print("-------------- Read Diagnostics --------------")
    # read_diagnostics_vin(diag_stub)
    #
    # print("-------------- Read Diagnostics --------------")
    # read_diagnostics_odb(diag_stub)
    #
    # print("-------------- Subsribe to LIN arbitratin BLOCKING --------------")
    # subscribe_to_arbitration(network_stub)
    #
    # print("-------------- Publish signals ONLY once--------------")
    # publish_signals(network_stub)
    #
    # print("-------------- SetFanSpeed --------------")
    # set_fan_speed(functional_stub, 8, 0)


if __name__ == "__main__":
    run()

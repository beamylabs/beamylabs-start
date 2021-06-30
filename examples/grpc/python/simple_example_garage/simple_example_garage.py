#!/usr/bin/env python3

import os
import random
import time

import grpc

import sys, getopt

sys.path.append("../common/generated")

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import diagnostics_api_pb2_grpc
import diagnostics_api_pb2

sys.path.append("../common")
import helper
from helper import *


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
import codecs

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
        upLink=upLink, downLink=downLink, serviceId=b"\x01", dataIdentifier=b"\x0C"
    )
    while True:
        try:
            response = stub.SendDiagnosticsQuery(request)
            print(response)
            # print(int.from_bytes(response.raw, 'big')) python 3.2
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


def run(argv):
    # Checks argument passed to script, simple_example_garage.py will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1"
    # Keep this port
    port = ":50051"
    try:
        opts, args = getopt.getopt(argv, "h", ["ip="])
    except getopt.GetoptError:
        print("Usage: simple_example_garage.py --ip <ip_address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: simple_example_garage.py --ip <ip_address>")
            sys.exit(2)
        elif opt == "--ip":
            ip = arg
    channel = grpc.insecure_channel(ip + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    diag_stub = diagnostics_api_pb2_grpc.DiagnosticsServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)

    upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)

    # print("-------------- Subsribe to fan speed BLOCKING --------------")
    # subscribe_to_fan_signal(network_stub)

    # print("-------------- Read Diagnostics --------------")
    # read_diagnostics_vin(diag_stub)
    #
    # print("-------------- Read Diagnostics --------------")
    read_diagnostics_odb(diag_stub)
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
    run(sys.argv[1:])

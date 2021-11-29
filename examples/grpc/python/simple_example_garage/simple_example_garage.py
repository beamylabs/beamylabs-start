#!/usr/bin/env python3

import os
import random
import time

import grpc

import sys
import argparse

sys.path.append("../common/generated")

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import diagnostics_api_pb2_grpc
import diagnostics_api_pb2


sys.path.append("../common")
sys.path.append("../signaltools")
import helper
from helper import *
from signalcreator import SignalCreator


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
    signal = signal_creator.signal("BenchC_c_2", namespace)
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
    namespace = "DiagnosticsCanInterface"
    upLink = signal_creator.signal("DiagReqBroadCastFrame_2015", namespace)
    # if you dont see any response try the other resp frames defined in the diagnostics dbc file.
    downLink = signal_creator.signal("DiagResFrame_2024", namespace)
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
    namespace = "DiagnosticsCanInterface"
    upLink = signal_creator.signal("DiagReqBroadCastFrame_2015", namespace)
    downLink = signal_creator.signal("DiagResFrame_2024", namespace)

    request = diagnostics_api_pb2.DiagnosticsRequest(
        upLink=upLink, downLink=downLink, serviceId=b"\x22", dataIdentifier=b"\xF1\x90"
    )
    try:
        response = stub.SendDiagnosticsQuery(request)
        print(response)
        print(binascii.hexlify(response.raw))
    except grpc._channel._Rendezvous as err:
        print(err)

def main(argv):
    parser = argparse.ArgumentParser(description="Provide address to Beambroker")
    parser.add_argument(
        "-ip",
        "--ip",
        type=str,
        help="IP address of the Beamy Broker",
        required=False,
        default="127.0.0.1",
    )
    parser.add_argument(
        "-port",
        "--port",
        type=str,
        help="grpc port used on Beamy Broker",
        required=False,
        default="50051",
    )
    args = parser.parse_args()
    run(args.ip, args.port)

def run(ip, port):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads."""
    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + ":" + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    diag_stub = diagnostics_api_pb2_grpc.DiagnosticsServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)

    upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)

    global signal_creator
    signal_creator = SignalCreator(system_stub)

    # print("-------------- Subsribe to fan speed BLOCKING --------------")
    # subscribe_to_fan_signal(network_stub)

    print("-------------- Read Diagnostics vin --------------")
    read_diagnostics_vin(diag_stub)
    
    print("-------------- Read Diagnostics BLOCKING--------------")
    read_diagnostics_odb(diag_stub)
    #
    # print("-------------- SetFanSpeed --------------")
    # set_fan_speed(functional_stub, 8, 0)


if __name__ == "__main__":
    main(sys.argv[1:])


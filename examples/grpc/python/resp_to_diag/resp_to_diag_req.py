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

sys.path.append("../common")
import helper
from helper import *

import binascii


def publish_signals(client_id, stub, diag_frame_resp):

    signal_with_payload = network_api_pb2.Signal(id=diag_frame_resp)
    signal_with_payload.raw = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    # signal_with_payload.raw = binascii.unhexlify("0102030405060708")
    publisher_info = network_api_pb2.PublisherConfig(
        clientId=client_id,
        signals=network_api_pb2.Signals(signal=[signal_with_payload]),
        frequency=0,
    )
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)


def subscribe_to_diag(client_id, stub, diag_frame_req, diag_frame_resp):
    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id,
        signals=network_api_pb2.SignalIds(signalId=[diag_frame_req]),
        onChange=False,
    )
    try:
        for response in stub.SubscribeToSignals(sub_info):
            print(response)
            print(binascii.hexlify(response.signal[0].raw))
            # here we could switch on the response.signal[0].raw which contains service id and did.
            publish_signals(client_id, stub, diag_frame_resp)
    except grpc._channel._Rendezvous as err:
        print(err)


def run(argv):
    # This script will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1"
    # Keep this port
    port = ":50051"
    try:
        opts, args = getopt.getopt(argv, "h", ["ip="])
    except getopt.GetoptError:
        print("Usage: resp_to_diag_req.py --ip <ip_address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: resp_to_diag_req.py --ip <ip_address>")
            sys.exit(2)
        elif opt == "--ip":
            ip = arg

    channel = grpc.insecure_channel(ip + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    client_id = common_pb2.ClientId(id="app_identifier")

    # If you need to change the id of the req/resp modify here configuration/can/diagnostics.dbc
    diag_frame_req = common_pb2.SignalId(
        name="DiagReqFrame_2016",
        namespace=common_pb2.NameSpace(name="DiagnosticsCanInterface"),
    )
    diag_frame_resp = signal = common_pb2.SignalId(
        name="DiagResFrame_2024",
        namespace=common_pb2.NameSpace(name="DiagnosticsCanInterface"),
    )

    upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)

    print(
        "-------------- Subscribe to diag_req, on request submit resp_frame --------------"
    )
    subscribe_to_diag(client_id, network_stub, diag_frame_req, diag_frame_resp)


if __name__ == "__main__":
    run(sys.argv[1:])


# try this by doing
#
# {"command": "subscribe", "signals": ["DiagResFrame_2024"], "namespace" : "DiagnosticsCanInterface"}
# {"command" : "write", "signals" : {"DiagReqFrame_2016": 3}, "namespace" : "DiagnosticsCanInterface"}

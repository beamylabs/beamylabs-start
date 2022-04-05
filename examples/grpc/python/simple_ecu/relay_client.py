#!/usr/bin/env python3

import os
import time
import binascii

import grpc

import sys, getopt
import argparse

sys.path.append("../common/generated")

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2


sys.path.append("../common")
sys.path.append("../signaltools")
import helper
from helper import *

from threading import Thread, Timer
import queue

from signalcreator import SignalCreator

signal_creator = None
q = queue.Queue()


def read_signals(stub, signal):
    """Read signals

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    signal : SignalId
        Object instance of class

    Returns
    -------
    Signals
        Object instance of class

    """
    try:
        read_info = network_api_pb2.SignalIds(signalId=[signal])
        return stub.ReadSignals(read_info)
    except grpc._channel._Rendezvous as err:
        print(err)


def publish_signals(client_id, stub, signals_with_payload, frequency=0):
    """Publish signals

    Parameters
    ----------
    client_id : ClientId
        Object instance of class
    stub : NetworkServiceStub
        Object instance of class
    signals_with_payload : Signal
        Object instance of class

    """
    publisher_info = network_api_pb2.PublisherConfig(
        clientId=client_id,
        signals=network_api_pb2.Signals(signal=signals_with_payload),
        frequency=frequency,
    )
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)


def printer(signals):
    for signal in signals:
        print(f"{signal.id.name} {signal.id.namespace.name} {get_value(signal)}")


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

def act_on_signal(client_id, stub, sub_signals, on_change, fun, on_subcribed=None):
    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id,
        signals=network_api_pb2.SignalIds(signalId=sub_signals),
        onChange=on_change,
    )
    try:
        subscripton = stub.SubscribeToSignals(sub_info, timeout=None)
        if on_subcribed:
            on_subcribed(subscripton)
        print("waiting for signal...")
        for subs_counter in subscripton:
            fun(subs_counter.signal)

    except grpc.RpcError as e:
        try:
            subscripton.cancel()
        except grpc.RpcError as e2:
            pass

    except grpc._channel._Rendezvous as err:
        print(err)
    # reload, alternatively non-existing signal
    print("subscription terminated")

def act_on_signal_persistant(client_id, stub, sub_signals, on_change, fun, on_subcribed=None):
    while True:
        # allow other client to reload
        act_on_signal(client_id, stub, sub_signals, on_change, fun, on_subcribed)

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


def power_on_client(system_stub, network_stub):
    def toggle_and_reply(client_id, network_stub, signals):
        def enable_relay(relay_signal):
            requested_state = get_value(relay_signal)
            assert 0 <= requested_state <= 2
            if requested_state == 0:
                print(f"relay {relay_signal.id.name} request no changed")
                return
            elif requested_state == 1:
                print(f"relay {relay_signal.id.name} request enable")
                # TODO GPIO code enable relay
                return
            elif requested_state == 2:
                print(f"relay {relay_signal.id.name} request disable")
                # TODO GPIO code disable relay
                return

        # control relay
        for relay_signal in signals:
            enable_relay(relay_signal)

        # send confirmation back
        publish_signals(
            client_id,
            network_stub,
            [
                signal_creator.signal_with_payload(
                    "Relays_resp_set", "physical_relays", ("integer", 1)
                )
            ],
        )

    client_id = common_pb2.ClientId(id="id_client_relay")
    subscriber = Thread(
        target=act_on_signal_persistant,
        args=(
            client_id,
            network_stub,
            # react to any relay in given frame
            signal_creator.signals_in_frame("Relay_00to07", "physical_relays"),
            # [signal_creator.signal("Relay01_enable_req", "physical_relays")],
            False,
            lambda signals: toggle_and_reply(client_id, network_stub, signals),
        ),
    )
    subscriber.start()
    return subscriber



def run(ip, port):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads."""
    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + ":" + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)

    upload_folder(system_stub, "configuration_udp")
    # upload_folder(system_stub, "configuration_lin")
    # upload_folder(system_stub, "configuration_can")
    # upload_folder(system_stub, "configuration_canfd")
    reload_configuration(system_stub)

    global signal_creator
    signal_creator = SignalCreator(system_stub)

    # Lists available signals
    configuration = system_stub.GetConfiguration(common_pb2.Empty())
    for networkInfo in configuration.networkInfo:
        print(
            "signals in namespace ",
            networkInfo.namespace.name,
            system_stub.ListSignals(networkInfo.namespace),
        )

    # Starting Threads

    # physical toggle power on using relay.
    thread = power_on_client(system_stub, network_stub)
    thread.join()

    time.sleep(10)
    


if __name__ == "__main__":
    main(sys.argv[1:])

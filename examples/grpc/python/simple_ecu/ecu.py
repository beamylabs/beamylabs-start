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

from signalcreator import SignalCreator

signal_creator = None


def read_signal(stub, signal):
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
    read_info = network_api_pb2.SignalIds(signalId=[signal])
    return stub.ReadSignals(read_info)


def publish_signals(client_id, stub, signals_with_payload):
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
        frequency=0,
    )
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)


increasing_counter = 0


def ecu_A(stub, pause):
    """Publishes a value, read other value (published by ecu_B)

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while True:
        global increasing_counter
        namespace = "ecu_A"
        clientId = common_pb2.ClientId(id="id_ecu_A")

        # Publishes value 'counter'
        counter_with_payload = signal_creator.signal_with_payload(
            "counter", namespace, ("integer", increasing_counter)
        )
        publish_signals(clientId, stub, [counter_with_payload])
        print("\necu_A, seed is ", increasing_counter)

        time.sleep(pause)

        # Read the other value 'counter_times_2' and output result
        counter_times_2 = signal_creator.signal("counter_times_2", namespace)

        read_counter_times_2 = read_signal(stub, counter_times_2)
        print(
            "ecu_A, (result) counter_times_2 is ",
            read_counter_times_2.signal[0].integer,
        )
        increasing_counter = (increasing_counter + 1) % 4


def read_on_timer(stub, signals, pause):
    """Simple reading with timer

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    signals : SignalId
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while True:
        read_info = network_api_pb2.SignalIds(signalId=signals)
        try:
            response = stub.ReadSignals(read_info)
            for signal in response.signal:
                print(f"ecu_B, (read) counter is {get_value(signal)}")
        except grpc._channel._Rendezvous as err:
            print(err)
        time.sleep(pause)


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


def act_on_signal(client_id, stub, sub_signals, on_change, fun):
    while True:
        sub_info = network_api_pb2.SubscriberConfig(
            clientId=client_id,
            signals=network_api_pb2.SignalIds(signalId=sub_signals),
            onChange=on_change,
        )
        try:
            subscripton = stub.SubscribeToSignals(sub_info, timeout=10)
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
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads.

    Parameters
    ----------
    argv : list
        Arguments passed when starting script

    """
    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + ":" + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)

    upload_folder(system_stub, "configuration_udp")
    # upload_folder(system_stub, "configuration_lin")
    # upload_folder(system_stub, "configuration_can")
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

    # ecu a, this is where we publish
    ecu_A_thread = Thread(
        target=ecu_A,
        args=(
            network_stub,
            1,
        ),
    )
    ecu_A_thread.start()

    # ecu b, we do this with lambda.
    ecu_b_client_id = common_pb2.ClientId(id="id_ecu_B")

    double_and_publish = lambda signals: (
        # we only have on signal, get it.
        # print(f"signals arrived {signals}"),
        print(f"ecu_B, (subscribe) counter is {get_value(signals[0])}"),
        publish_signals(
            ecu_b_client_id,
            network_stub,
            [
                signal_creator.signal_with_payload(
                    "counter_times_2", "ecu_B", ("integer", get_value(signals[0]) * 2)
                )
            ],
        ),
    )

    ecu_B_sub_thread = Thread(
        target=act_on_signal,
        args=(
            ecu_b_client_id,
            network_stub,
            [signal_creator.signal("counter", "ecu_B")],
            True,  # only report when signal changes
            double_and_publish,
        ),
    )
    ecu_B_sub_thread.start()

    # ecu b, additonaly, read using timer.
    read_signals = [signal_creator.signal("counter", "ecu_B")]
    ecu_read_on_timer = Thread(
        target=read_on_timer, args=(network_stub, read_signals, 1)
    )
    ecu_read_on_timer.start()


if __name__ == "__main__":
    main(sys.argv[1:])

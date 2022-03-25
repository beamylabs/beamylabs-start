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


def ecu_A(stub, pause):
    """Publishes a value, read other value (published by ecu_B)

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    increasing_counter = 0
    namespace = "ecu_A"
    clientId = common_pb2.ClientId(id="id_ecu_A")
    while True:

        print("\necu_A, seed is ", increasing_counter)
        # Publishes value 'counter'

        publish_signals(
            clientId,
            stub,
            [
                # signal_creator.signal_with_payload(
                #     "counter", namespace, ("integer", increasing_counter)
                # ),
                # add any number of signals here, make sure that all signals/frames are unique.
                signal_creator.signal_with_payload(
                    "MasterReq", namespace, ("raw", binascii.unhexlify("0a0b0c0d0a0b0c0d")), False
                ),
                # to provide manual headers (relevant for lin only)
                # signal_creator.signal_with_payload(
                #     "MasterReq", namespace, ("arbitration", True), False
                # ),
                # signal_creator.signal_with_payload(
                #     "SlaveResp", namespace, ("arbitration", True), False
                # ),
            ],
        )
        publish_signals(
            clientId,
            stub,
            [
                # signal_creator.signal_with_payload(
                #     "counter", namespace, ("integer", increasing_counter)
                # ),
                # add any number of signals here, make sure that all signals/frames are unique.
                # signal_creator.signal_with_payload(
                #     "MasterReq", namespace, ("raw", binascii.unhexlify("0a0b0c0d0a0b0c0d")), False
                # ),
                # to provide manual headers (relevant for lin only)
                signal_creator.signal_with_payload(
                    "MasterReq", namespace, ("arbitration", True), False
                )
                # signal_creator.signal_with_payload(
                #     "SlaveResp", namespace, ("arbitration", True), False
                # ),
            ],
        )

        publish_signals(
            clientId,
            stub,
            [
                # signal_creator.signal_with_payload(
                #     "counter", namespace, ("integer", increasing_counter)
                # ),
                # add any number of signals here, make sure that all signals/frames are unique.
                # signal_creator.signal_with_payload(
                #     "MasterReq", namespace, ("raw", binascii.unhexlify("0a0b0c0d0a0b0c0d")), False
                # ),
                # to provide manual headers (relevant for lin only)
                signal_creator.signal_with_payload(
                    "SlaveResp", namespace, ("arbitration", True), False
                )
                # signal_creator.signal_with_payload(
                #     "SlaveResp", namespace, ("arbitration", True), False
                # ),
            ],
        )

        time.sleep(pause)

        # Read the other value 'counter_times_2' and output result

        # read_signal_response = read_signals(
        #     stub, signal_creator.signal("counter_times_2", namespace)
        # )
        # for signal in read_signal_response.signal:
        #     print(f"ecu_A, (result) {signal.id.name} is {get_value(signal)}")
        # increasing_counter = (increasing_counter + 1) % 4


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
                print(f"ecu_B, (read) {signal.id.name} is {get_value(signal)}")
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


def double_and_publish(network_stub, client_id, trigger, signals):
    for signal in signals:
        print(f"ecu_B, (subscribe) {signal.id.name} {get_value(signal)}")
        if signal.id == trigger:
            publish_signals(
                client_id,
                network_stub,
                [
                    signal_creator.signal_with_payload(
                        "counter_times_2", "ecu_B", ("integer", get_value(signal) * 2)
                    ),
                    # add any number of signals/frames here
                    # signal_creator.signal_with_payload(
                    #     "TestFr04", "ecu_B", ("raw", binascii.unhexlify("0a0b0c0d")), False
                    # )
                ],
            )


def run(ip, port):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads."""
    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + ":" + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)

    # upload_folder(system_stub, "configuration_udp")
    upload_folder(system_stub, "configuration_lin")
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

    # ecu b, we do this with lambda refering to double_and_publish.
    ecu_b_client_id = common_pb2.ClientId(id="id_ecu_B")

    def log_signals(signals):
        for signal in signals:
            print(get_value(signal))
    
    ecu_B_sub_thread = Thread(
        target=act_on_signal,
        args=(
            ecu_b_client_id,
            network_stub,
            [
                signal_creator.signal("SlaveResp", "ecu_A"),
                # here you can add any signal from any namespace
                # signal_creator.signal("TestFr04", "ecu_B"),
            ],
            True,  # True: only report when signal changes
            lambda signals: log_signals(signals),
            lambda subscripton: (q.put(("id_ecu_B", subscripton)))
        ),
    )
    ecu_B_sub_thread.start()
    # wait for subscription to settle
    ecu, subscription = q.get()

    # ecu a, this is where we publish, and
    ecu_A_thread = Thread(
        target=ecu_A,
        args=(
            network_stub,
            1,
        ),
    )
    ecu_A_thread.start()

    # ecu b, bonus, periodically, read using timer.
    # signals = [
    #     signal_creator.signal("counter", "ecu_B"),
    #     # add any number of signals from any namespace
    #     # signal_creator.signal("TestFr04", "ecu_B"),
    # ]
    # ecu_read_on_timer = Thread(target=read_on_timer, args=(network_stub, signals, 1))
    # ecu_read_on_timer.start()

    # once we are done we could cancel subscription
    # subscription.cancel()


if __name__ == "__main__":
    main(sys.argv[1:])

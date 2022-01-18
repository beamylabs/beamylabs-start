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
import statistics

from signalcreator import SignalCreator

signal_creator = None
q = queue.Queue()
time_stamp_ref = {}
time_diff_a_a = []
time_diff_a_b = []


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
        print(
            f"time diff {signal.id.name} {signal.id.namespace.name} {get_value(signal)} {signal.timestamp}"
        )


def ecu_tester(stub, client_id, namespace, pause):
    global time_diff_a_a
    global time_diff_a_b

    increasing_counter = 0
    while True:

        publish_signals(
            client_id,
            stub,
            [
                signal_creator.signal_with_payload(
                    "counter", namespace, ("integer", increasing_counter)
                ),
            ],
        )

        time.sleep(pause)
        increasing_counter = (increasing_counter + 1) % 4

        if len(time_diff_a_a) == 100:
            print(
                "time_diff_a_a measured %s values, mean is: %s, stdev is: %s"
                % (
                    len(time_diff_a_a),
                    statistics.mean(time_diff_a_a),
                    statistics.stdev(time_diff_a_a),
                )
            )
            time_diff_a_a = []
            print(
                "time_diff_a_b measured %s values, mean is: %s, stdev is: %s"
                % (
                    len(time_diff_a_b),
                    statistics.mean(time_diff_a_b),
                    statistics.stdev(time_diff_a_b),
                )
            )
            time_diff_a_b = []


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


# TD;LR
# Measure time for signal to travel form ecu_tester_id to ecu_under_test_id
#
# we specify three different clients on this system which we seperate using client id
# ecu_tester_id: operates on ecu_A: send stimuli to the DUT.
# ecu_under_test_id: operates on ecu_B: on received message counter it emits count_times_2.
# time_measurer_id: operates on ecu_A and collects the reference time (emit of counter) and return or counter_times_2
# 
# About client_id
# emitted signals from a specific client_id does not return to the same client, thus all above client_id are unique.
# every client can work on any number of namespaces
def run(ip, port):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads."""
    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + ":" + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)

    # upload_folder(system_stub, "configuration_udp")
    # upload_folder(system_stub, "configuration_lin")
    upload_folder(system_stub, "configuration_can")
    # upload_folder(system_stub, "configuration_canfd")
    reload_configuration(system_stub)

    global signal_creator
    signal_creator = SignalCreator(system_stub)

    # Starting Threads

    #####################################################################
    # ECU under test (DUT) is located on namespace ecu_B which and it's
    # specified behaviour is just to to bounce (emit) counter_times_2 as soon as
    # counter arrive
    ecu_under_test_id = common_pb2.ClientId(id="ecu_under_test_id")
    ecu_under_test_namespace = "ecu_B"

    def bounce(network_stub, client_id, trigger, signals):
        global time_stamp_ref
        global time_diff_a_b
        for signal in signals:
            if signal.id == trigger:
                publish_signals(
                    client_id,
                    network_stub,
                    [
                        signal_creator.signal_with_payload(
                            "counter_times_2",
                            ecu_under_test_namespace,
                            ("integer", get_value(signal)),
                        ),
                    ],
                )
                if time_stamp_ref != {} and (
                    get_value(signal) == get_value(time_stamp_ref)
                ):
                    print(
                        f"time difference (counter @ {time_stamp_ref.id.namespace.name} -> counter @ {signal.id.namespace.name}) is {signal.timestamp - time_stamp_ref.timestamp}"
                    )
                    time_diff_a_b.append(signal.timestamp - time_stamp_ref.timestamp)

    Thread(
        target=act_on_signal,
        args=(
            ecu_under_test_id,
            network_stub,
            [
                # this is what triggers our bounce
                signal_creator.signal("counter", ecu_under_test_namespace),
            ],
            False,  # True: only report when signal changes
            lambda signals: bounce(
                network_stub,
                ecu_under_test_id,
                signal_creator.signal("counter", ecu_under_test_namespace),
                signals,
            ),
            lambda subscripton: (q.put((ecu_under_test_id, subscripton))),
        ),
    ).start()
    # wait for subscription to settle
    ecu, subscription = q.get()
    #####################################################################

    #####################################################################
    # set up an subscriber which listens to emitted signal and received.
    # NOTE: This subscriber needs to have unique "Client_id", which is different
    # from the publishing client, in order to not be filtered away
    time_measurer_id = common_pb2.ClientId(id="time_measurer_id")
    time_measurer_namespace = "ecu_A"

    def on_subscription(trigger_a, trigger_b, signals):
        global time_stamp_ref
        global time_diff_a_a
        for signal in signals:
            if signal.id == trigger_a:
                time_stamp_ref = signal
            elif signal.id == trigger_b and (
                time_stamp_ref != {}
                and (get_value(signal) == get_value(time_stamp_ref))
            ):
                print(
                    f"time difference (counter @ {time_measurer_namespace} -> counter_times_2 @ {time_measurer_namespace}) is {signal.timestamp - time_stamp_ref.timestamp}"
                )
                time_diff_a_a.append(signal.timestamp - time_stamp_ref.timestamp)
            else:
                time_stamp_ref = {}

    Thread(
        target=act_on_signal,
        args=(
            time_measurer_id,
            network_stub,
            [
                # this is what we will emit.
                signal_creator.signal("counter", time_measurer_namespace),
                # this will bounce back form ecu_under_test_id
                signal_creator.signal("counter_times_2", time_measurer_namespace),
            ],
            False,  # True: only report when signal changes
            lambda signals: on_subscription(
                signal_creator.signal("counter", time_measurer_namespace),
                signal_creator.signal("counter_times_2", time_measurer_namespace),
                signals,
            ),
            lambda subscripton: (q.put((time_measurer_id, subscripton))),
        ),
    ).start()
    # wait for subscription to settle
    ecu, subscription = q.get()
    #####################################################################

    #####################################################################
    # Emit signals form ecu_a which till trigger ECU under test

    ecu_tester_id = common_pb2.ClientId(id="ecu_tester_id")
    ecu_tester_namespace = "ecu_A"

    Thread(
        target=ecu_tester,
        args=(network_stub, ecu_tester_id, ecu_tester_namespace, 0.05),
    ).start()
    #####################################################################


if __name__ == "__main__":
    main(sys.argv[1:])

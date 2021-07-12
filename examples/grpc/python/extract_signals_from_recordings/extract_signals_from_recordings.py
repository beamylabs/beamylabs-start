#!/usr/bin/python
"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import os
import time
import binascii

import grpc

import sys, getopt
import csv

sys.path.append("../common/generated")

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import traffic_api_pb2
import traffic_api_pb2_grpc

sys.path.append("../common")
import helper
from helper import *

from threading import Thread, Event

exit_event = Event()


def playback_resources():
    return [
        (
            "custom_can_A",  # destination namespace
            "recordings/traffic_A.log",  # upload file location
            "recordings/uploaded_traffic_A.log",  # location on destination
        ),
        (   "custom_can_B", 
            "recordings/traffic_B.log", 
            "recordings/uploaded_traffic_B.log"
        ),
    ]


def signal_list():
    signals = [
        ("Speed", "custom_can_B"),  # signal/frame, namespace
        ("VehicleSpeed", "custom_can_B"),
        ("VehicleSpeedInt", "custom_can_B"),
        ("CompartmentTemp", "custom_can_B"),
        ("VehicleMotionSafe", "custom_can_A"),
    ]
    return list(
        map(
            lambda entry: common_pb2.SignalId(
                name=entry[0], namespace=common_pb2.NameSpace(name=entry[1])
            ),
            signals,
        )
    )

# subscribe to signals
def monitor_streams(traffic_stub, networks):
    a = len(networks)
    try:
        for traffic_status in traffic_stub.PlayTrafficStatus(common_pb2.Empty()):
            for traffic_info in traffic_status.playbackInfo:
                print("traffic status is %s " % (traffic_info))
                if traffic_info.playbackMode.mode == traffic_api_pb2.Mode.STOP:
                    a = a - 1
            if a == 0:
                print("All streams stopped")
                sys.exit(0)

    except grpc._channel._Rendezvous as err:
        print(err)

# subscribe to signals
def ecu_B_subscribe(stub, signals, onChange, fun):
    client_id = common_pb2.ClientId(id="id_ecu_B")

    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id,
        signals=network_api_pb2.SignalIds(signalId=signals),
        onChange=onChange,
    )
    try:
        for subscription in stub.SubscribeToSignals(sub_info):
            for signal in subscription.signal:
                # print("ecu_B, %s with value %s " % (signal.id, signal))
                fun(signal)

    except grpc._channel._Rendezvous as err:
        print(err)


def create_playback_config(entry):
    playbackConfig = traffic_api_pb2.PlaybackConfig(
        fileDescription=system_api_pb2.FileDescription(path=entry["path"]),
        namespace=common_pb2.NameSpace(name=entry["namespace"]),
    )
    return traffic_api_pb2.PlaybackInfo(
        playbackConfig=playbackConfig,
        playbackMode=traffic_api_pb2.PlaybackMode(mode=entry["mode"]),
    )


def stop_playback():
    channel = grpc.insecure_channel(ip)
    traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
    playback_list = list(
        map(
            lambda x: {
                "namespace": x[0],
                "path": x[2],
                "mode": traffic_api_pb2.Mode.STOP,
            },
            playback_resources(),
        )
    )
    status = traffic_stub.PlayTraffic(
        traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(create_playback_config, playback_list))
        )
    )
    print("Stop traffic status is ", status)


def exit_handler(signum, frame):
    exit_event.set()


def get_value(signal):
    if signal.raw != b"":
        return "0x" + binascii.hexlify(signal.raw).decode("ascii")
    elif signal.HasField("integer"):
        return signal.integer
    elif signal.HasField("double"):
        return signal.double
    elif signal.HasFiles("arbitration"):
        return signal.arbitration
    else:
        return "empty"


def csv_logger(csv_writer, signal):
    csv_writer.writerow(
        [signal.timestamp, signal.id.namespace.name, signal.id.name, get_value(signal)]
    )


def run(argv):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads.
    Parameters
    ----------
    argv : list
        Arguments passed when starting script
    """
    # Checks argument passed to script, ecu.py will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1"
    # Keep this port
    port = ":50051"
    try:
        opts, args = getopt.getopt(argv, "h", ["ip="])
    except getopt.GetoptError:
        print("Usage: ecu.py --ip <ip_address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: ecu.py --ip <ip_address>")
            sys.exit(2)
        elif opt == "--ip":
            ip = arg

    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)

    upload_folder(system_stub, "configuration_custom_udp")
    reload_configuration(system_stub)

    thread_monitor_streams = Thread(
        target=monitor_streams,
        args=(traffic_stub, playback_resources()),
    )
    thread_monitor_streams.start()

    # get namespace avalibale
    namespaces_and_signals = {}
    configuration = system_stub.GetConfiguration(common_pb2.Empty())
    for networkInfo in configuration.networkInfo:
        namespaces_and_signals[networkInfo.namespace.name] = system_stub.ListSignals(
            networkInfo.namespace
        ).frame

    for namespace, resource, upload_dest in playback_resources():
        upload_file(system_stub, resource, upload_dest)

    # Subscribe
    signals = signal_list()

    # first check if signals exist, if not - complain
    for signalid in signals:
        assert signalid.namespace.name in namespaces_and_signals, "Namespace %s defined by signal %s not defined" % (signalid.namespace.name, signalid)
        assert is_signal_declared(
            signalid, namespaces_and_signals[signalid.namespace.name]
        ), "Requested signals does not exist, signal: %s" % (signalid)

    # prepare csv file
    target_filename = "logger.csv"
    csv_file = open(target_filename, "w", newline="")
    csv_writer = csv.writer(
        csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    logger_fun = lambda signal: csv_logger(csv_writer, signal)

    thread_subscribe = Thread(
        target=ecu_B_subscribe,
        args=(network_stub, signal_list(), False, logger_fun),
    )
    thread_subscribe.start()

    # playback
    playback_list = list(
        map(
            lambda x: {
                "namespace": x[0],
                "path": x[2],
                "mode": traffic_api_pb2.Mode.PLAY,
            },
            playback_resources(),
        )
    )

    playback_infos = traffic_api_pb2.PlaybackInfos(
        playbackInfo=list(map(create_playback_config, playback_list))
    )
    status = traffic_stub.PlayTraffic(playback_infos)
    assert status == playback_infos, "playback failed %s" % (status)

    print(
        'producing %s, stop by hitting crtl-c. Try "tail -f %s"'
        % (target_filename, target_filename)
    )

    thread_monitor_streams.join()
    csv_file.close()
    print("done!")


if __name__ == "__main__":
    run(sys.argv[1:])

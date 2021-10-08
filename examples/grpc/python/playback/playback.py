#!/usr/bin/env python3

import os
import time
import binascii

import grpc

import sys, getopt

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

import signal
from threading import Thread, Timer, Event

exit_event = Event()


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
    Signal
        Object instance of class

    """
    read_info = network_api_pb2.SignalIds(signalId=[signal])
    return stub.ReadSignals(read_info)


def ecu_B_read(stub, pause):
    """Read some value published by ecu_A

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while not exit_event.is_set():
        namespace = "custom_can"
        client_id = common_pb2.ClientId(id="id_ecu_B")

        # Read value 'SteerAngle'
        steer_angle = common_pb2.SignalId(
            name="SteerAngle", namespace=common_pb2.NameSpace(name=namespace)
        )
        response = read_signal(stub, steer_angle)
        print("ecu_B, (read) SteerAngle is ", response.signal[0].double)

        time.sleep(pause)


def ecu_B_subscribe_(stub):
    """Subscribe to a value published by ecu_A and output value

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class

    """

    namespace = "custom_can"
    client_id = common_pb2.ClientId(id="id_ecu_B")

    # Subscribe to value 'SteerAngle'
    steer_angle = common_pb2.SignalId(
        name="SteerAngle", namespace=common_pb2.NameSpace(name=namespace)
    )
    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id,
        signals=network_api_pb2.SignalIds(signalId=[steer_angle]),
        onChange=True,
    )

    # Output subscribed signal
    try:
        for subs_counter in stub.SubscribeToSignals(sub_info):
            # For clean exit when stopping script
            if exit_event.is_set():
                break
            print("ecu_B, (subscribe) SteerAngle is ", subs_counter.signal[0])
    except grpc._channel._Rendezvous as err:
        print(err)


def read_on_timer(stub, signals, pause):
    """Simple reading with timer, logs on purpose tabbed with double space

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    signals : SignalId
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while not exit_event.is_set():
        read_info = network_api_pb2.SignalIds(signalId=signals)
        try:
            response = stub.ReadSignals(read_info)
            for signal in response.signal:
                print(
                    "  read_on_timer " + signal.id.name + " value " + str(signal.double)
                )
        except grpc._channel._Rendezvous as err:
            print(err)

        time.sleep(pause)


def create_playback_config(item):
    """Creating configuration for playback

    Parameters
    ----------
    item : dict
        Dictionary containing 'path', 'namespace' and 'mode'

    Returns
    -------
    PlaybackInfo
        Object instance of class

    """
    playbackConfig = traffic_api_pb2.PlaybackConfig(
        fileDescription=system_api_pb2.FileDescription(path=item["path"]),
        namespace=common_pb2.NameSpace(name=item["namespace"]),
    )
    return traffic_api_pb2.PlaybackInfo(
        playbackConfig=playbackConfig,
        playbackMode=traffic_api_pb2.PlaybackMode(mode=item["mode"]),
    )


def stop_playback():
    """Stop ongoing playback"""
    channel = grpc.insecure_channel(ip + port)
    traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
    for playback in playbacklist:
        playback["mode"] = traffic_api_pb2.Mode.STOP

    status = traffic_stub.PlayTraffic(
        traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(create_playback_config, playbacklist))
        )
    )
    print("Stop traffic status is ", status)


def exit_handler(signum, frame):
    """Custom handler for exit of script

    Parameters
    ----------
    signum : int
        Signal number defined in pythons standard signal library
    frame : frame
        Object instance of class, stack frame

    """
    exit_event.set()
    time.sleep(0.5)
    stop_playback()


def run(argv):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads.

    Parameters
    ----------
    argv : list
        Arguments passed when starting script

    """
    global ip
    global port
    global playbacklist
    # Checks argument passed to script, playback.py will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1"
    # Keep this port
    port = ":50051"
    try:
        opts, args = getopt.getopt(argv, "h", ["ip="])
    except getopt.GetoptError:
        print("Usage: playback.py --ip <ip_address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: playback.py --ip <ip_address>")
            sys.exit(2)
        elif opt == "--ip":
            ip = arg

    # To do a clean exit of the script on CTRL+C
    signal.signal(signal.SIGINT, exit_handler)

    # Setting up stubs and configuration
    channel = grpc.insecure_channel(ip + port)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    # check_license(system_stub)

    upload_folder(system_stub, "configuration_custom_udp")
    reload_configuration(system_stub)
    # Give us some time to see it all went according to plan
    time.sleep(1)

    # Lists available signals
    configuration = system_stub.GetConfiguration(common_pb2.Empty())
    for networkInfo in configuration.networkInfo:
        print(
            "signals in namespace ",
            networkInfo.namespace.name,
            system_stub.ListSignals(networkInfo.namespace),
        )

    ecu_B_thread_subscribe = Thread(target=ecu_B_subscribe, args=(network_stub,))
    ecu_B_thread_subscribe.start()

    # playback_status = traffic_stub.StartPlayback(playback_interator([{"namespace": "test_can", "path": "recordings/candump.log", "mode": 0}, {"namespace": "test_can", "path": "recordings/candump.log", "mode": 0}]))
    # playback_status = traffic_stub.StartPlayback(playback_interator([
    #     {"namespace": "test_can", "path": "recordings/candump.log", "mode": traffic_api_pb2.PlaybackMode.PLAY},
    #     {"namespace": "ecu_A", "path": "recordings/candump.log", "mode": traffic_api_pb2.PlaybackMode.PLAY}
    #     ]))
    # for entries in playback_status:
    #     print(entries)

    upload_file(
        system_stub,
        "configuration_udp/recordings/candump.log",
        "recordings/candump_uploaded.log",
    )

    time.sleep(1)
    recordlist = [
        {
            "namespace": "test_can",
            "path": "recordings/candump_uploaded_recorded.log",
            "mode": traffic_api_pb2.Mode.RECORD,
        },
    ]
    status_record = traffic_stub.PlayTraffic(
        traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(create_playback_config, recordlist))
        )
    )
    print("record traffic result is ", status_record)

    playbacklist = [
        {
            "namespace": "test_can",
            "path": "recordings/candump_uploaded.log",
            "mode": traffic_api_pb2.Mode.PLAY,
        },
        {
            "namespace": "ecu_A",
            "path": "recordings/candump.log",
            "mode": traffic_api_pb2.Mode.PLAY,
        },
        {
            "namespace": "ecu_C",
            "path": "recordings/candump_.log",
            "mode": traffic_api_pb2.Mode.PLAY,
        },
    ]
    # expect candump_.log does not exist, this errorstring will be returned
    status = traffic_stub.PlayTraffic(
        traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(create_playback_config, playbacklist))
        )
    )
    print("play traffic result is ", status)

    time.sleep(1)

    # now stop recording and download the recorded file
    download_file(
        system_stub,
        "recordings/candump_uploaded_recorded.log",
        "candump_uploaded_recorded_downloaded.log",
    )
    print("file is now downloaded")

    # Starting Threads
    ecu_B_thread_read = Thread(
        target=ecu_B_read,
        args=(
            network_stub,
            1,
        ),
    )
    ecu_B_thread_read.start()

    # ecu_B_thread_subscribe  = Thread(target = ecu_B_subscribe_, args = (network_stub,))
    # ecu_B_thread_subscribe.start()

    # read_signals = [common_pb2.SignalId(name="SteerAngle", namespace=common_pb2.NameSpace(name = "custom_can")), common_pb2.SignalId(name="SteerAngleSpeed", namespace=common_pb2.NameSpace(name = "custom_can"))]
    # ecu_read_on_timer  = Thread(target = read_on_timer, args = (network_stub, read_signals, 2))
    # ecu_read_on_timer.start()


if __name__ == "__main__":
    run(sys.argv[1:])

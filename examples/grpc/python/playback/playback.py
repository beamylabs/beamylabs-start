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
    read_info = network_api_pb2.SignalIds(signalId=[signal])
    return stub.ReadSignals(read_info)


# read some value published by ecu_a (playback)
def ecu_B_read(stub, pause):
    while True:
        namespace = "custom_can"
        client_id = common_pb2.ClientId(id="id_ecu_B")
        counter = common_pb2.SignalId(
            name="SteerAngle", namespace=common_pb2.NameSpace(name=namespace)
        )
        read_counter = read_signal(stub, counter)
        print("ecu_B, (read) SteerAngle is ", read_counter.signal[0].double)

        if exit_event.is_set():
            stop_playback()
            sys.exit(2)

        time.sleep(pause)


# subscribe to some value published by ecu_a (playback), prints signal
def ecu_B_subscribe_(stub):
    namespace = "custom_can"
    client_id = common_pb2.ClientId(id="id_ecu_B")
    counter = common_pb2.SignalId(
        name="SteerAngle", namespace=common_pb2.NameSpace(name=namespace)
    )

    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id,
        signals=network_api_pb2.SignalIds(signalId=[counter]),
        onChange=True,
    )
    try:
        for subs_counter in stub.SubscribeToSignals(sub_info):
            print("ecu_B, (subscribe) SteerAngle is ", subs_counter.signal[0])

            if exit_event.is_set():
                stop_playback()
                sys.exit(2)

    except grpc._channel._Rendezvous as err:
        print(err)


# simple reading
# logs on purpose tabbed with double space
def read_on_timer(stub, signals, pause):
    while True:
        if exit_event.is_set():
            stop_playback()
            sys.exit(2)

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


def create_playback_config(thing):
    playbackConfig = traffic_api_pb2.PlaybackConfig(
        fileDescription=system_api_pb2.FileDescription(path=thing["path"]),
        namespace=common_pb2.NameSpace(name=thing["namespace"]),
    )
    return traffic_api_pb2.PlaybackInfo(
        playbackConfig=playbackConfig,
        playbackMode=traffic_api_pb2.PlaybackMode(mode=thing["mode"]),
    )


def playback_interator(playbacklist):
    for x in [
        1
    ]:  # one this suggests that we can modify this stream and move it to another state
        playbackrequest = list(map(create_playback_config, playbacklist))
        yield traffic_api_pb2.PlaybackInfos(playbackInfo=playbackrequest)


def stop_playback():
    channel = grpc.insecure_channel(ip)
    traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
    playbacklist = [
        {
            "namespace": "custom_can",
            "path": "recordings/candump_uploaded.log",
            "mode": traffic_api_pb2.Mode.STOP,
        }
    ]
    status = traffic_stub.PlayTraffic(
        traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(create_playback_config, playbacklist))
        )
    )
    print("Stop traffic status is ", status)


def exit_handler(signum, frame):
    exit_event.set()


def run(argv):
    global ip
    # This script will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1:50051"
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

    # Setup
    channel = grpc.insecure_channel(ip)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    # check_license(system_stub)

    upload_folder(system_stub, "configuration_custom_udp")
    reload_configuration(system_stub)
    # Give us some time to see it all went according to plan
    time.sleep(1)

    # list available signals
    configuration = system_stub.GetConfiguration(common_pb2.Empty())
    for networkInfo in configuration.networkInfo:
        print(
            "signals in namespace ",
            networkInfo.namespace.name,
            system_stub.ListSignals(networkInfo.namespace),
        )

    upload_file(
        system_stub,
        "configuration_custom_udp/recordings/traffic.log",
        "recordings/candump_uploaded.log",
    )
    # NOTE: If changing this playbacklist, also update playbacklist in function 'stop_playback'
    playbacklist = [
        {
            "namespace": "custom_can",
            "path": "recordings/candump_uploaded.log",
            "mode": traffic_api_pb2.Mode.PLAY,
        }
    ]
    status = traffic_stub.PlayTraffic(
        traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(create_playback_config, playbacklist))
        )
    )
    print("play traffic result is ", status)

    # Read
    ecu_B_thread_read = Thread(
        target=ecu_B_read,
        args=(
            network_stub,
            1,
        ),
    )
    ecu_B_thread_read.start()

    # Subscribe
    # ecu_B_thread_subscribe  = Thread(target = ecu_B_subscribe_, args = (network_stub,))
    # ecu_B_thread_subscribe.start()

    # Read list of signals on timer
    # read_signals = [common_pb2.SignalId(name="SteerAngle", namespace=common_pb2.NameSpace(name = "custom_can")), common_pb2.SignalId(name="SteerAngleSpeed", namespace=common_pb2.NameSpace(name = "custom_can"))]
    # ecu_read_on_timer  = Thread(target = read_on_timer, args = (network_stub, read_signals, 2))
    # ecu_read_on_timer.start()


if __name__ == "__main__":
    run(sys.argv[:1])

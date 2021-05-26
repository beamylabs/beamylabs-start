"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import os
import time
import binascii

import grpc

import sys
sys.path.append('../common/generated')

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2

sys.path.append('../common')
import helper
from helper import *

from threading import Thread, Timer

def publish_signals(client_id, stub, signals_with_payload, freq):
    publisher_info = network_api_pb2.PublisherConfig(clientId = client_id, signals=network_api_pb2.Signals(signal=signals_with_payload), frequency = freq)
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)

# ecu_A publised a set of signals with a given freq
def ecu_A_publish(stub, signals_with_payload, freq):
    global increasing_counter
    clientId = common_pb2.ClientId(id="id_ecu_A")
    publish_signals(clientId, stub, signals_with_payload, freq)

# subscribe to some value (counter) published by ecu_a, double and send value back to eca_a (counter_times_2)
def ecu_B_subscribe(stub, signals, onChange):
    client_id = common_pb2.ClientId(id="id_ecu_B")

    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=signals), onChange=onChange)
    try:
        for subscription in stub.SubscribeToSignals(sub_info):
            for signal in subscription.signal:
                # print("ecu_B, (signal id) ", signal.id)
                print("ecu_B, %s with value %s " % (signal.id, signal))
            
    except grpc._channel._Rendezvous as err:
            print(err)

def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    # check_license(system_stub)
    
    upload_folder(system_stub, "configuration_udp")
    # upload_folder(system_stub, "configuration_lin")
    # upload_folder(system_stub, "configuration_can")
    # upload_folder(system_stub, "configuration_canfd")
    reload_configuration(system_stub)

    # list available signals
    # configuration = system_stub.GetConfiguration(common_pb2.Empty())
    # for networkInfo in configuration.networkInfo:
    #     print("signals in namespace ", networkInfo.namespace.name, system_stub.ListSignals(networkInfo.namespace))

    namespace = "ecu_A"
    namespace=common_pb2.NameSpace(name = namespace)
 
    frames = all_frames(system_stub, namespace)
    print("all frames ", frames)

    signals = all_signals_in_frame(system_stub, frames[1])
    print("signal in frame ", signals[0])

    signal = common_pb2.SignalId(name=signals[0].name, namespace=namespace)
    signal_with_payload = network_api_pb2.Signal(id = signal, integer = 2)

    signal2 = common_pb2.SignalId(name=signals[1].name, namespace=namespace)
    signal2_with_payload = network_api_pb2.Signal(id = signal2, integer = 1)

    ecu_A_publish_thread  = Thread(target = ecu_A_publish, args = (network_stub, [signal_with_payload, signal2_with_payload], 10))
    ecu_A_publish_thread.start()


    # subscribing code...
    namespace_sub = "ecu_B"
    namespace_sub=common_pb2.NameSpace(name = namespace_sub)

    signal = common_pb2.SignalId(name=signals[0].name, namespace=namespace_sub)
    signal2 = common_pb2.SignalId(name=signals[1].name, namespace=namespace_sub)

    on_change = False
    ecu_B_thread_subscribe  = Thread(target = ecu_B_subscribe, args = (network_stub, [signal, signal2], on_change))
    ecu_B_thread_subscribe.start()

if __name__ == '__main__':
    run()

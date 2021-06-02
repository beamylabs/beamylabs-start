"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import os
import time
import binascii

import grpc

import sys, getopt
sys.path.append('../common/generated')

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import traffic_api_pb2
import traffic_api_pb2_grpc

sys.path.append('../common')
import helper
from helper import *

from threading import Thread, Timer

def publish_signals(stub, client_id, signals_with_payload, freq):
    publisher_info = network_api_pb2.PublisherConfig(clientId = client_id, signals=network_api_pb2.Signals(signal=signals_with_payload), frequency = freq)
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)

def ecu_master_subscribe(stub, client_id, signals, onChange):
    global increasing_counter

    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=signals), onChange=onChange)
    try:
        for subscription in stub.SubscribeToSignals(sub_info):
            for signal in subscription.signal:
                if not signal.HasField("arbitration"):
                    print("master, %s with value %s " % (signal.id, signal))
            
    except grpc._channel._Rendezvous as err:
            print(err)

def ecu_slave_subscribe(stub, client_id, signals, onChange):
    global increasing_counter

    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=signals), onChange=onChange)
    try:
        for subscription in stub.SubscribeToSignals(sub_info):
            for signal in subscription.signal:
                if not signal.HasField("arbitration"):
                    print("slave, %s with value %s " % (signal.id, signal))
            
    except grpc._channel._Rendezvous as err:
            print(err)

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
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    # check_license(system_stub)
    
    upload_folder(system_stub, "configuration_lin")
    reload_configuration(system_stub)

    # grace period to let clients time to pull their configuration 
    time.sleep(5)

    clientId = common_pb2.ClientId(id="this_python_app_identifier")
    
    # slave, prepare to answer to diag request, this gets loaded pening in the transiever (waiting for aribitration)
    namespace_slave = "ecu_B"
    signal = common_pb2.SignalId(name="SlaveResp", namespace=common_pb2.NameSpace(name = namespace_slave))
    signal_with_payload = network_api_pb2.Signal(id = signal, raw = b"\x81\x09\x0a\x0b\x0c\x0d\x0e\x0f")
    publish_signals(network_stub, clientId, [signal_with_payload], 0)

    print("Slave is ready to reply to diag request %s" %(signal_with_payload))

    # master, subscribe to answer from client (just listen)
    namespace_master = "ecu_A"

    frame = common_pb2.SignalId(name="SlaveResp", namespace=common_pb2.NameSpace(name = namespace_master))
    # frame = common_pb2.SignalId(name="counter_times_2", namespace=common_pb2.NameSpace(name = namespace_master))
    ecu_m_subscribe  = Thread(target = ecu_master_subscribe, args = (network_stub, clientId, [frame], False))
    ecu_m_subscribe.daemon = True # allow this thread to be automatically stopped on exit.
    ecu_m_subscribe.start()

    # Just listen from slave, for debug purposes
    # frame2 = common_pb2.SignalId(name="MasterReq", namespace=common_pb2.NameSpace(name = namespace_slave))
    # ecu_s_subscribe  = Thread(target = ecu_slave_subscribe, args = (network_stub, clientId, [frame, frame2], False))
    # ecu_s_subscribe.start()
    
    # # send arbitration from master (not needed arbitration is enabled inte inderfaces.json), expect nothing back! (send arbitration)
    #
    # signal = common_pb2.SignalId(name="SlaveResp", namespace=common_pb2.NameSpace(name = namespace_master))
    # signal_with_payload = network_api_pb2.Signal(id = signal, arbitration = True)
    # publish_signals(network_stub, clientId, [signal_with_payload], 0)

    print("sent %s from master expect nothing back" % (signal_with_payload))
    time.sleep(1)

    # send master request, now with propriate NAD, DEVS2 has NAD 0x81 (which is the fist byte below)
    signal = common_pb2.SignalId(name="MasterReq", namespace=common_pb2.NameSpace(name = namespace_master))
    signal_with_payload = network_api_pb2.Signal(id = signal, raw = b"\x81\x02\x03\x04\x05\x06\x07\x08")
    publish_signals(network_stub, clientId, [signal_with_payload], 0)

    print("sent %s from master expect nothing back, but client is now ready to reply" % (signal_with_payload))
    time.sleep(1)

    # # send arbitration from master, expect answer since nad is matching
    # signal = common_pb2.SignalId(name="SlaveResp", namespace=common_pb2.NameSpace(name = namespace_master))
    # signal_with_payload = network_api_pb2.Signal(id = signal, arbitration = True)
    # publish_signals(network_stub, clientId, [signal_with_payload], 0)

    print("sent %s from master expect ANSWER" % (signal_with_payload))
    time.sleep(3)


    # send master request, now with another NAD, make sure client doesn't (which is the fist byte below)
    signal = common_pb2.SignalId(name="MasterReq", namespace=common_pb2.NameSpace(name = namespace_master))
    signal_with_payload = network_api_pb2.Signal(id = signal, raw = b"\x82\x02\x03\x04\x05\x06\x07\x08")
    publish_signals(network_stub, clientId, [signal_with_payload], 0)


    # send arbitration from master, expect nothing back (nad is not matching)!
    signal = common_pb2.SignalId(name="SlaveResp", namespace=common_pb2.NameSpace(name = namespace_master))
    signal_with_payload = network_api_pb2.Signal(id = signal, arbitration = True)
    publish_signals(network_stub, clientId, [signal_with_payload], 0)

    print("sent %s from master NOT expecting ANSWER" % (signal_with_payload))
    time.sleep(1)

    print("still quiet.... done")

if __name__ == "__main__":
    run(sys.argv[1:])
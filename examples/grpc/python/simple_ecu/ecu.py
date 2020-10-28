"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import os
import random
import time

import grpc

import sys
sys.path.append('generated')

import network_api_pb2
import network_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2


import hashlib
import base64

from threading import Thread, Timer
##################### START BOILERPLATE ####################################################


def get_sha256(file):
        f = open(file,"rb")
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        return readable_hash

# 20000 as in infinity
def generate_data(file, dest_path, chunk_size, sha256):
    for x in range(0, 20000):
        if x == 0:
                fileDescription = system_api_pb2.FileDescription(sha256 = sha256, path = dest_path)
                yield system_api_pb2.FileUploadRequest(fileDescription = fileDescription)
        else:
                buf = file.read(chunk_size)
                if not buf:
                        break
                yield system_api_pb2.FileUploadRequest(chunk = buf)   

def upload_file(stub, path, dest_path):
     sha256 = get_sha256(path)
     print(sha256)
     file = open(path, "rb")  

     upload_iterator = generate_data(file, dest_path, 1000000, sha256)
     response = stub.UploadFile(upload_iterator)
     print("uploaded", path, response)

from glob import glob

def upload_folder(system_stub, folder):
     files = [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*')) if not os.path.isdir(y)]
     for file in files:
            upload_file(system_stub, file, file.replace(folder, ""))

def reload_configuration(system_stub):
      request = common_pb2.Empty()
      response = system_stub.ReloadConfiguration(request, timeout=60000)
      print(response)



##################### END BOILERPLATE ####################################################

def read_signal(stub, signal):
    read_info = network_api_pb2.SignalIds(signalId=[signal])
    return stub.ReadSignals(read_info)

def publish_signal(client_id, stub, signal, value):
    signal_with_payload = network_api_pb2.Signal(id = signal)
    signal_with_payload.integer = value
    publisher_info = network_api_pb2.PublisherConfig(clientId = client_id, signals=network_api_pb2.Signals(signal=[signal_with_payload]), frequency = 0)
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)

increasing_counter = 0
# ecu_A publish some value (counter), read other value (counter_times_2) (which is published by ecu_B)
def ecu_A(stub, pause):
    while True:
        global increasing_counter
        namespace = "DiagnosticsCanInterface"
        clientId = common_pb2.ClientId(id="id_ecu_A")
        counter = common_pb2.SignalId(name="DiagResFrame_2024", namespace=common_pb2.NameSpace(name = namespace))
        publish_signal(clientId, stub, counter, increasing_counter)
        
        # read the other value and output result
        counter_times_2 = common_pb2.SignalId(name="counter_times_2", namespace=common_pb2.NameSpace(name = namespace))
        read_counter_times_2 = read_signal(stub, counter_times_2)

        print("ecu_A, counter_times_2 is ", read_counter_times_2.signal[0].integer)
        increasing_counter = (increasing_counter + 1) % 10
        time.sleep(0.1)

# read some value (counter) published by ecu_a, double and send value (counter_times_2)
def ecu_B_read(stub, pause):
    while True:
        namespace = "DiagnosticsCanInterface"
        client_id = common_pb2.ClientId(id="id_ecu_B")
        counter = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = namespace))
        read_counter = read_signal(stub, counter)
        print("ecu_B, counter is ", read_counter.signal[0].integer)

        counter_times_2 = common_pb2.SignalId(name="counter_times_2", namespace=common_pb2.NameSpace(name = namespace))
        publish_signal(client_id, stub, counter_times_2, read_counter.signal[0].integer * 2)        
        time.sleep(pause)

def ecu_B_subscribe(stub):
    namespace = "ecu_B"
    client_id = common_pb2.ClientId(id="id_ecu_B")
    counter = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = namespace))

    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=[counter]), onChange=False)
    try:
        for subs_counter in stub.SubscribeToSignals(sub_info):
            print("ecu_B, counter is ", subs_counter.signal[0].integer)
            counter_times_2 = common_pb2.SignalId(name="counter_times_2", namespace=common_pb2.NameSpace(name = namespace))
            publish_signal(client_id, stub, counter_times_2, subs_counter.signal[0].integer * 2)    
            
    except grpc._channel._Rendezvous as err:
            print(err)

def read_on_timer(client_id, stub, signal, pause):
    while True:
        read_info = network_api_pb2.SignalIds(signalId=[signal])
        try:
                signals = stub.ReadSignals(read_info)
        except grpc._channel._Rendezvous as err:
                print(err)
        print("signal read is ", signals, signals.signal[0].integer)
        time.sleep(pause)


def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    
#     upload_folder(system_stub, "configuration_udp")
    # upload_folder(system_stub, "configuration")
    # reload_configuration(system_stub)

    ecu_A_thread  = Thread(target = ecu_A, args = (network_stub, 1,))
    ecu_A_thread.start()

    # ecu_B_thread_read  = Thread(target = ecu_B_read, args = (network_stub, 1,))
    # ecu_B_thread_read.start()

#     ecu_B_thread_subscribe  = Thread(target = ecu_B_subscribe, args = (network_stub,))
#     ecu_B_thread_subscribe.start()


if __name__ == '__main__':
    run()

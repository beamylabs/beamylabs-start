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

def publish_signals(client_id, stub, diag_frame_resp):
    signal_with_payload = network_api_pb2.Signal(id = diag_frame_resp)
    signal_with_payload.raw = b'\x01x02x03x04x05x06x07x08'
    publisher_info = network_api_pb2.PublisherConfig(clientId = client_id, signals=network_api_pb2.Signals(signal=[signal_with_payload]), frequency = 0)
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)



import binascii
def subscribe_to_diag(client_id, stub, diag_frame_req, diag_frame_resp):
    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=[diag_frame_req]), onChange=False)
    try:
        for response in stub.SubscribeToSignals(sub_info):
            print(response)   
            print(binascii.hexlify(response.signal[0].raw))
            # here we could switch on the response.signal[0].raw which contains service id and did.     
            publish_signals(client_id, stub, diag_frame_resp)
    except grpc._channel._Rendezvous as err:
            print(err)

counter = 0

def publish_on_timer(client_id, stub, signal, pause):
    global counter
    while True:
        signal_with_payload = network_api_pb2.Signal(id = signal)
        signal_with_payload.integer = counter % 100
        publisher_info = network_api_pb2.PublisherConfig(clientId = client_id, signals=network_api_pb2.Signals(signal=[signal_with_payload]), frequency = 0)
        try:
                stub.PublishSignals(publisher_info)
        except grpc._channel._Rendezvous as err:
                print(err)
        time.sleep(pause)
        counter = counter + 1


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
    channel = grpc.insecure_channel('192.168.1.33:50051')
#     channel = grpc.insecure_channel('192.168.4.1:50051')
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    

# If you need to change the id of the req/resp modify here configuration/can/diagnostics.dbc 
#     diag_frame_req = common_pb2.SignalId(name="DiagReqFrame_2016", namespace=common_pb2.NameSpace(name = "DiagnosticsCanInterface"))
#     diag_frame_resp = signal = common_pb2.SignalId(name="DiagResFrame_2024", namespace=common_pb2.NameSpace(name = "DiagnosticsCanInterface"))
 
    upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)

    # let ecu_A write value at some given intervall
    
    client_id_ecu_A = common_pb2.ClientId(id="ecu_A")
    signal_on_ecu_A = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = "ecu_A"))

    ecu_A_thread = Thread(target = publish_on_timer, args = (client_id_ecu_A, network_stub, signal_on_ecu_A, 1, ))
    ecu_A_thread.start()

    # let ecu_B read the value muliply by 2 and send back result
    client_id_ecu_B = common_pb2.ClientId(id="ecu_B")
    signal_on_ecu_B = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = "ecu_B"))
    ecu_B_thread = Thread(target = read_on_timer, args = (client_id_ecu_B, network_stub, signal_on_ecu_B, 1, ))
    ecu_B_thread.start()

     

#     print("-------------- Subscribe to diag_req, on request submit resp_frame --------------")
#     subscribe_to_diag(client_id, network_stub, diag_frame_req, diag_frame_resp)


if __name__ == '__main__':
    run()


# try this by doing
# 
# {"command": "subscribe", "signals": ["DiagResFrame_2024"], "namespace" : "DiagnosticsCanInterface"}
# {"command" : "write", "signals" : {"DiagReqFrame_2016": 3}, "namespace" : "DiagnosticsCanInterface"}

# Copyright 2020 Beamy

import os
import random
import time

import grpc

import sys
sys.path.append('generated')

import network_api_pb2
import network_api_pb2_grpc
import functional_api_pb2
import functional_api_pb2_grpc
import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import diagnostics_api_pb2_grpc
import diagnostics_api_pb2

import binascii
import socket
import struct

def publish_signals(stub):
    source = common_pb2.ClientId(id="app_identifier")

    namespace = common_pb2.NameSpace(name = "ChassisCANhs")
    signal = common_pb2.SignalId(name="SteerWhlAgSafe", namespace=namespace)

    signal_with_payload = network_api_pb2.Signal(id = signal)
    signal_with_payload.double = 4.4
    publisher_info = network_api_pb2.PublisherConfig(clientId = source, signals=network_api_pb2.Signals(signal=[signal_with_payload]), frequency = 0)
    try:
        stub.PublishSignals(publisher_info)
        time.sleep(0.3)
    except grpc._channel._Rendezvous as err:
        print(err)


# port 2004 is mapped for ChassisCANhs, SteerWhlAgSafe is in frame 64
def send_udp():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = 0x1234567812345678
    while True:
        frame_id = 64
        payload = payload + 0x8123456781234
        package = struct.pack(">IBq", frame_id, 8, payload)
        soc.sendto(package, ("127.0.0.1", 2004))
        time.sleep(0.3)

# from pysine import sine   

# def subscribe_to_signal(stub):
#     source = common_pb2.ClientId(id="app_identifier")
# #     signal = common_pb2.SignalId(name="EngN", namespace=common_pb2.NameSpace(name = "ChassisCANhs"))
# #     signal = common_pb2.SignalId(name="EngNSafeEngNGrdt", namespace=common_pb2.NameSpace(name = "ChassisCANhs"))
#     signal = common_pb2.SignalId(name="VehSpdLgtSafe", namespace=common_pb2.NameSpace(name = "ChassisCANhs"))
#     sub_info = network_api_pb2.SubscriberConfig(clientId=source, signals=network_api_pb2.SignalIds(signalId=[signal]), onChange=False)
#     try:
#         for response in stub.SubscribeToSignals(sub_info):
#             speed = response.signal[0].double * 100
#             sine(frequency=speed, duration=0.005)
#             print(response.signal[0].double)
#     except grpc._channel._Rendezvous as err:
#             print(err)


##################### START BOILERPLATE ####################################################

import hashlib
import posixpath
import ntpath

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

     # make sure path is unix style (necessary for windows, and does no harm om linux)
     upload_iterator = generate_data(file, dest_path.replace(ntpath.sep, posixpath.sep), 1000000, sha256)
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

def run():
#     channel = grpc.insecure_channel('192.168.1.82:50051')
    channel = grpc.insecure_channel('192.168.1.184:50051')
    functional_stub = functional_api_pb2_grpc.FunctionalServiceStub(channel)
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    diag_stub = diagnostics_api_pb2_grpc.DiagnosticsServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)


    print("-------------- upload configuration folder and reload system --------------")
    upload_folder(system_stub, "../../../../configurations/demo-torslanda")
#     upload_folder(system_stub, "../../../../configurations/mountainview")
#     upload_folder(system_stub, "../../../../configurations/vanilla-osx")
    reload_configuration(system_stub)

    print("-------------- publish signal using udp blocking --------------")
    while True:
        send_udp() 

#     print("-------------- publish signal over publish api blocking --------------")
#     while True:
#         publish_signals(network_stub) 

#     print("-------------- publish signal blocking --------------")
#     while True:
#         publish_signals(network_stub) 

#     print("-------------- Subscribe and play blocking --------------")
#     subscribe_to_signal(diag_stub)
    
    
    # print("-------------- Read Diagnostics --------------")
    # read_diagnostics_vin(diag_stub)
    #
    # print("-------------- Read Diagnostics --------------")
    # read_diagnostics_odb(diag_stub)
    #
    # print("-------------- Subsribe to LIN arbitratin BLOCKING --------------")
    # subscribe_to_arbitration(network_stub)

if __name__ == '__main__':
    run()

# start server
# open browser, look at tree
# look at interfaces.json code /Users/aleksandarfilipov/Projects/beamy/signalbroker-server/configuration/interfaces.json
# upload new configuration
# look at new configuration code /Users/aleksandarfilipov/Projects/beamy/signalbroker-server/configuration/configuration_custom_A/interfaces.json
# set up subscription
# look at data (nothing happens)
# send signal
#    using signal
#    telnet 
#    udp
# look at data use telnet, use browser
# FakeCanConnection.start_playback
# look at data in browser, start subscription
# 


# try subscribe to SteerWhlAgSafe, BrkPedlPsd, DrvrDesDir on chassiscan

# try subscribe to VehMtnStCntr on bodycan
# telnet 127.0.0.1 4040 
# {"command" : "list", "namespace": "BodyCANhs", "userdata" : "your_data"}
# {"command" : "read", "signals" : ["SteerWhlAgSafe"], "namespace": "ChassisCANhs", "userdata" : "your_data"}
# {"command": "subscribe", "signals": ["SteerWhlAgSafe"], "namespace" : "ChassisCANhs"}
# {"command" : "write", "signals" : {"SteerWhlAgSafe": 3}, "namespace" : "ChassisCANhs"}

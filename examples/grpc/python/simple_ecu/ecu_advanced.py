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

import binascii

from threading import Thread, Timer
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

def check_license(system_stub):
    status = system_stub.GetLicenseInfo(common_pb2.Empty()).status
    assert status == system_api_pb2.LicenseStatus.VALID, "Check your license, status is: %d" % status

import requests
import json
import base64

# re-request a license. By default uses the same email (requestId) as before
# hash will be found in your mailbox
def request_license(system_stub, id=None):
    if id == None:
        id = (system_stub.GetLicenseInfo(common_pb2.Empty()).requestId).encode("utf-8")
        assert id != '', "no old id avaliable, provide your email"
    requestMachineId = system_stub.GetLicenseInfo(common_pb2.Empty()).requestMachineId
    requestId = system_stub.GetLicenseInfo(common_pb2.Empty()).requestId
    body = {"id": requestId.encode("utf-8"), "machine_id": json.loads(requestMachineId)}
    resp_request = requests.post('https://www.beamylabs.com/requestlicense', json = {"licensejsonb64": base64.b64encode(json.dumps(body))})
    assert resp_request.status_code == requests.codes.ok, "Response code not ok, code: %d" % (resp_request.status_code)
    print("License requested check your mail: ", id)

# using your hash, upload your license (remove the dashes) use the same email (requestId) address as before
def download_license(system_stub, hash_without_dashes):
    requestId = system_stub.GetLicenseInfo(common_pb2.Empty()).requestId
    resp_fetch = requests.post('https://www.beamylabs.com/fetchlicense', json = {"id": requestId, "hash": hash_without_dashes})
    assert resp_fetch.status_code == requests.codes.ok, "Response code not ok, code: %d" % (resp_fetch.status_code)
    license_info = resp_fetch.json()
    license_bytes = license_info['license_data'].encode('utf-8')
    # you agree to license and conditions found here https://www.beamylabs.com/license/
    system_stub.SetLicense(system_api_pb2.License(termsAgreement = True, data = license_bytes))
    
##################### END BOILERPLATE ####################################################

def read_signal(stub, signal):
    read_info = network_api_pb2.SignalIds(signalId=[signal])
    return stub.ReadSignals(read_info)

def publish_signals(client_id, stub, signals_with_payload):
    publisher_info = network_api_pb2.PublisherConfig(clientId = client_id, signals=network_api_pb2.Signals(signal=signals_with_payload), frequency = 0)
    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        print(err)

increasing_counter = 0
# ecu_A publish some value (counter, and testFr06_Child02, TestFr04), then it reads other value (counter_times_2) (which has been published by ecu_B)
def ecu_A(stub, pause):
    while True:
        global increasing_counter
        namespace = "ecu_A"
        clientId = common_pb2.ClientId(id="id_ecu_A")
        # counter
        counter = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = namespace))
        counter_with_payload = network_api_pb2.Signal(id = counter, integer = increasing_counter)
        # TestFr06_Child02 - another signal
        testFr06_Child02 = common_pb2.SignalId(name="TestFr06_Child02", namespace=common_pb2.NameSpace(name = namespace))
        testFr06_Child02_with_payload = network_api_pb2.Signal(id = testFr06_Child02, integer = increasing_counter+1)
        # TestFr04 - now a frame
        testFr04 = common_pb2.SignalId(name="TestFr04", namespace=common_pb2.NameSpace(name = namespace))
        testFr04_with_payload = network_api_pb2.Signal(id = testFr04, integer = increasing_counter+2)

        print("\necu_A, seed is ", increasing_counter)
        publish_signals(clientId, stub, [counter_with_payload, testFr06_Child02_with_payload, testFr04_with_payload])
        
        time.sleep(pause)

        # read the other value and output result
        counter_times_2 = common_pb2.SignalId(name="counter_times_2", namespace=common_pb2.NameSpace(name = namespace))
        read_counter_times_2 = read_signal(stub, counter_times_2)

        print("ecu_A, (result) counter_times_2 is ", read_counter_times_2.signal[0].integer)
        increasing_counter = (increasing_counter + 1) % 10

# read some value (counter) published by ecu_a
def ecu_B_read(stub, pause):
    while True:
        namespace = "ecu_B"
        client_id = common_pb2.ClientId(id="id_ecu_B")
        counter = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = namespace))
        read_counter = read_signal(stub, counter)
        print("ecu_B, (read) counter is ", read_counter.signal[0].integer)
        
        time.sleep(pause)

# subscribe to some value (counter) published by ecu_a, double and send value back to eca_a (counter_times_2)
def ecu_B_subscribe(stub):
    namespace = "ecu_B"
    client_id = common_pb2.ClientId(id="id_ecu_B")
    counter = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = namespace))

    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=[counter]), onChange=False)
    try:
        for subs_counter in stub.SubscribeToSignals(sub_info):
            print("ecu_B, (subscribe) counter is ", subs_counter.signal[0].integer)
            counter_times_2 = common_pb2.SignalId(name="counter_times_2", namespace=common_pb2.NameSpace(name = namespace))
            signal_with_payload = network_api_pb2.Signal(id = counter_times_2, integer = subs_counter.signal[0].integer * 2)
            publish_signals(client_id, stub, [signal_with_payload])
            
    except grpc._channel._Rendezvous as err:
            print(err)


# shows possibiliy to subscribe to same signal muliple times
# also using array to subscribe to additonal signals
# logs on purpose tabbed with single space
def ecu_B_subscribe_2(stub):
    namespace = "ecu_B"
    # specify some signals
    client_id = common_pb2.ClientId(id="id_ecu_B")
    counter = common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = namespace))
    testFr06_Child02 = common_pb2.SignalId(name="TestFr06_Child02", namespace=common_pb2.NameSpace(name = namespace))
    testFr04 = common_pb2.SignalId(name="TestFr04", namespace=common_pb2.NameSpace(name = namespace))

    sub_info = network_api_pb2.SubscriberConfig(clientId=client_id, signals=network_api_pb2.SignalIds(signalId=[counter, testFr06_Child02, testFr04]), onChange=False)
    try:
        for response in stub.SubscribeToSignals(sub_info):
            # since we subscribe to a set of signal we need to check which arrived.
            for signal in response.signal:
                if (signal.id.name == "counter"):
                    print(" ecu_B, (subscribe_2) counter is ", signal.integer)
                if (signal.id.name == "TestFr06_Child02"):
                    print(" ecu_B signal: " + signal.id.name + " arrived: " + str(signal.integer))
                if (signal.id.name == "TestFr04"):
                    print(" ecu_B, (subscribe_2) raw is ", binascii.hexlify(signal.raw))
            
    except grpc._channel._Rendezvous as err:
            print(err)

# simple reading
# logs on purpose tabbed with double space
def read_on_timer(stub, signals, pause):
    while True:
        read_info = network_api_pb2.SignalIds(signalId=signals)
        try:
                response = stub.ReadSignals(read_info)
                for signal in response.signal:
                    print("  read_on_timer " + signal.id.name + " value " + str(signal.integer))
        except grpc._channel._Rendezvous as err:
                print(err)
        time.sleep(pause)

def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    network_stub = network_api_pb2_grpc.NetworkServiceStub(channel)
    system_stub = system_api_pb2_grpc.SystemServiceStub(channel)
    check_license(system_stub)
    # request_license(system_stub)
    # download_license(system_stub, "your_emailed_hash_without_quotes")
    
    upload_folder(system_stub, "configuration_udp")
    # upload_folder(system_stub, "configuration")
    reload_configuration(system_stub)

    # list available signals
    configuration = system_stub.GetConfiguration(common_pb2.Empty())
    for networkInfo in configuration.networkInfo:
        print("signals in namespace ", networkInfo.namespace.name, system_stub.ListSignals(networkInfo.namespace))

    ecu_A_thread  = Thread(target = ecu_A, args = (network_stub, 1,))
    ecu_A_thread.start()

    ecu_B_thread_read  = Thread(target = ecu_B_read, args = (network_stub, 1,))
    ecu_B_thread_read.start()

    ecu_B_thread_subscribe  = Thread(target = ecu_B_subscribe, args = (network_stub,))
    ecu_B_thread_subscribe.start()

    ecu_B_thread_subscribe_2  = Thread(target = ecu_B_subscribe_2, args = (network_stub,))
    ecu_B_thread_subscribe_2.start()

    read_signals = [common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = "ecu_A")), common_pb2.SignalId(name="TestFr06_Child02", namespace=common_pb2.NameSpace(name = "ecu_A"))]
    ecu_read_demo  = Thread(target = read_on_timer, args = (network_stub, read_signals, 10))
    ecu_read_demo.start()



if __name__ == '__main__':
    run()

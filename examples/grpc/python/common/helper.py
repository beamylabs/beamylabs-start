##################### START BOILERPLATE ####################################################

import system_api_pb2
import system_api_pb2_grpc
import common_pb2
import os

import hashlib
import posixpath
import ntpath
import itertools

def get_sha256(file):
        f = open(file,"rb")
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        return readable_hash

def generate_data(file, dest_path, chunk_size, sha256):
    for x in itertools.count(start=0):
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
     assert len(files) != 0, "Specified upload folder is empty or does not exist, provided folder was: %s" % folder
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
        id = system_stub.GetLicenseInfo(common_pb2.Empty()).requestId
        assert id != '', "no old id available, provide your email"
    requestMachineId = system_stub.GetLicenseInfo(common_pb2.Empty()).requestMachineId
    body = {"id": id, "machine_id": json.loads(requestMachineId)}
    resp_request = requests.post('https://www.beamylabs.com/requestlicense', json = {"licensejsonb64": base64.b64encode(json.dumps(body).encode("utf-8")).decode()})
    assert resp_request.status_code == requests.codes.ok, "Response code not ok, code: %d" % (resp_request.status_code)
    print("License requested, check your mail: ", id)

# using your hash, upload your license (remove the dashes) use the same email (requestId) address as before
def download_and_install_license(system_stub, hash, id=None):
    if id == None:
        id = system_stub.GetLicenseInfo(common_pb2.Empty()).requestId
        assert id.encode("utf-8") != '', "no old id avaliable, provide your email"
    resp_fetch = requests.post('https://www.beamylabs.com/fetchlicense', json = {"id": id, "hash": hash.replace('-', '')})
    assert resp_fetch.status_code == requests.codes.ok, "Response code not ok, code: %d" % (resp_fetch.status_code)
    license_info = resp_fetch.json()
    license_bytes = license_info['license_data'].encode('utf-8')
    # you agree to license and conditions found here https://www.beamylabs.com/license/
    system_stub.SetLicense(system_api_pb2.License(termsAgreement = True, data = license_bytes))

# checks if signal is declared. 
# signal = common_pb2.SignalId(name="MasterReq", namespace=common_pb2.NameSpace(name = "ecu_A")
def is_signal_declared(system_stub, signal):
    signals = []
    for frame_entry in system_stub.ListSignals(signal.namespace).frame:
        signals.append(frame_entry.signalInfo.id)
        for signal_entry in frame_entry.childInfo:
            signals.append(signal_entry.id)
    found = signal in signals
    return found

##################### END BOILERPLATE ####################################################

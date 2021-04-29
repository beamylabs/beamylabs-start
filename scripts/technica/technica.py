# invoke with sudo as in sudo python3 technica.py
# dependent on scapy, to install: pip3 install scapy

import sys
from scapy.all import *

def dispatch(packet):
#   print("sending")
   try: 
      load = packet[0][1].load
      size = len(load)
      clientSocket.send((2021).to_bytes(2, byteorder='big', signed=False) + size.to_bytes(2, byteorder='big', signed=False) + load)
   except:
      print('skipping package') 

def run():
   if len(sys.argv) < 3:
      print ("Usage: sudo python3 technica.py iface_name port")
      print ("example")
      print ("technica.py enp0s31f6 51111")
      quit()

   s = socket.socket();
   target = ('127.0.0.1', int(sys.argv[2]));
   s.bind(target);
   s.listen();
   print("listening")

   while True:
      print("waiting for client")
      global clientSocket
      (clientSocket_local, clientAddress) = s.accept();
      clientSocket = clientSocket_local
      print("connected")
      sniff(prn=dispatch, iface=sys.argv[1])

if __name__ == '__main__':
    run()
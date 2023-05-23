import socket
from QKE import QKE
from XOR import XOR

'''
A simple transmitter that establishes a secret key with a 
receiver using an emulation of Quantum Key Exchange.

Messages are then encoded with an XOR cipher before sending.

Created by Luke Finlayson, 1557835
'''

class Transmitter:
    def __init__(self, verbose=None):
      self.qke = QKE()
      self.verbose = verbose

    '''
    Connect to a receiver listening on the given port
    '''
    def connect(self, port) -> bool:
       # Attempt to connect to a receiver
      try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', port))

        return True
      except:
        print("[Transmitter] Failed to connect.")
        return False
      
    def establishKey(self, length):
      # Send a stream of qubits to the receiver
      for i in range(length):
        value, polarisation = self.qke.generateQubit()

        # def. sending an actual qubit and not just the values...
        self.socket.send(bytes([value, polarisation]))
      
      # Send the end of stream identifier
      self.socket.send(bytes([0, 2]))

      # Exchange polarisations
      polarisation = self.qke.polarisations

      receivedPolarisations = [i for i in self.socket.recv(length)]
      self.socket.send(bytes(self.qke.polarisations))

      self.key = self.qke.createKey(receivedPolarisations)
    
    def sendMessage(self, message: str):
      if not self.xor:
        self.xor = XOR(self.key)

      encoded = self.xor.encode(message)
      self.socket.send(encoded)

    def close(self):
      self.socket.close()
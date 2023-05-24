import socket
from qke import QKE
from xor import XOR

'''
A simple transmitter that establishes a secret key with a 
receiver using an emulation of Quantum Key Exchange.

Messages are then encoded with an XOR cipher before sending.

Created by Luke Finlayson, 1557835
'''

class Transmitter:
    def __init__(self, port):
      self.port = port
      self.qke = QKE()
      self.xor = None

    '''
    Connect to a receiver listening on the given port
    '''
    def connect(self) -> bool:
       # Attempt to connect to a receiver
      try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', self.port))

        return True
      except:
        print("[Transmitter] Failed to connect.")
        return False
      
    '''
    Attempt to connect to a receiver and establish
    a new secret key.
    '''
    def establishKey(self, length):
      self.connect()

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

      self.close()
    
    '''
    Attempt to send a message to a receiver encoded
    with the previously established secret key.
    '''
    def sendMessage(self, message: str):
      # First attempt to open connection
      if not self.connect():
        return

      if not self.xor:
        self.xor = XOR(self.key)

      encoded = self.xor.encode(message)
      self.socket.send(encoded)

      self.close()

    def close(self):
      self.socket.close()


'''
Simple main process so transmitter can be run as a 
standalone program.

Note: no error handling
'''
if __name__ == "__main__":
  port = int(input("Use port: "))
  transmitter = Transmitter(port)

  while True:
    action = input("\n[Options]\n\t(1) Establish Key\n\t(2) Send Message\n\t(*) Quit\nChoose action: ")

    match action:
      case "1":
        length = int(input("\nUse length: "))
        transmitter.establishKey(length)
      case "2":
        message = input("\nEnter message: ")
        transmitter.sendMessage(message)
      case _:
        break

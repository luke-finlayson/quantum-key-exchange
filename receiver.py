import socket

from qke import QKE
from qubit import Qubit
from xor import XOR

'''
A simple receiver that establishes a secret key with a
transmitter using an emulation of Quantum Key Exchange.

Messages received are then decoded with an XOR cipher.

Created by Luke Finlayson, 1557835
'''

class Receiver:
    def __init__(self):
      self.qke = QKE()
      self.xor = None

    '''
    Create the socket server and bind to a
    random port.

    Returns the port that was assigned
    '''
    def open(self) -> int:
      try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", 0))
        self.socket.listen()

        return self.socket.getsockname()[1]
      except:
        print("[Receiver] Failed to establish socket")

    '''
    Listen for an accept socket connections, executing a callback 
    function on connection and returning the result of the callback
    '''
    def listen(self, callback):
      conn, addr = self.socket.accept()
      res = None

      with conn:
        res = callback(conn)
        conn.close()

      return res

    '''
    Attempt to establish a new secret key with a socket connection
    '''
    def establishKey(self, conn: socket.socket):
      while True:
        data = conn.recv(2)

        if not data:
          print("[Receiver] Connection terminated unexpectedly")
          break
        
        # wow how would I ever be able to measure this 'qubit' without changing it...
        value, polarisation = [int(i) for i in data]

        # Check for end of stream symbol
        if polarisation == 2:
          break

        self.qke.receiveQubit(Qubit(value, polarisation))         

      # Now we have our list of measured qubits - send the random polarisations back
      polarisations = self.qke.polarisations
      conn.send(bytes(polarisations))

      receivedPolarisations = [i for i in conn.recv(len(polarisations))]

      self.key = self.qke.createKey(receivedPolarisations)

    '''
    Receive a message sent by a socket connection,
    returning the message decoded by the XOR cipher
    '''
    def receive(self, conn: socket.socket):
      if not self.xor:
        self.xor = XOR(self.key)
      
      res = []

      while True:
        data = conn.recv(1024)

        if not data:
          break

        res.extend(data)

      return self.xor.decode(bytes(res))


'''
Simple main process so the receiver can be run
as a standalone program

Note: no error handling
'''
if __name__ == "__main__":
  receiver = Receiver()
  print("Listening on port ", receiver.open())

  while True:
    action = input("\n[Options]\n\t(1) Establish Key\n\t(2) Wait for message\nChoose action: ")

    match action:
      case "1":
        receiver.listen(receiver.establishKey)
      case "2":
        print("\n", receiver.listen(receiver.receive))
      case _:
        break
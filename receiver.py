import socket

from QKE import QKE
from Qubit import Qubit

class Receiver:
    def __init__(self):
      self.qke = QKE()

    def open(self) -> int:
      try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", 0))

        return self.socket.getsockname()[1]
      except:
        print("[Receiver] Failed to establish socket")

    def listen(self, callback) -> int:
      self.socket.listen()
      conn, addr = self.socket.accept()

      with conn:
        callback(conn)
        conn.close()

      self.socket.close()

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
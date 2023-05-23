import random
from Qubit import Qubit

class QKE:
    def __init__(self):
        self.polarisations = []
        self.values = []

    def generateQubit(self) -> tuple([int, int]):
        # Generate random value and polarisation
        v = random.randint(0, 1)
        p = random.randint(0, 1)

        # qubit = Qubit(v, p)

        # Record the polarisation and values
        self.polarisations.append(p)
        self.values.append(v)
        return v, p

    def receiveQubit(self, qubit):
        # Choose a random polarisation
        p = random.randint(0, 1)

        # Measure and record the qubit
        v = qubit.measure(p)

        self.polarisations.append(p)
        self.values.append(v)

    def createKey(self, receivedPolarisations: list):
        # Error check just in case - although receiver-transmitter should be synced by this point
        if (len(receivedPolarisations) != len(self.polarisations)):
            print("Mismatched lengths")
            return None

        key = []

        for i in range(len(self.polarisations)):
          match = self.nxor(self.polarisations[i], receivedPolarisations[i])
          
          if match:
              key.append(self.values[i])

        return key

    def nxor(self, a: int, b: int):
        return (a & b) | ((not a) & (not b))

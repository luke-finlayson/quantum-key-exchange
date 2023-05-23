from threading import Thread
import pytest

from QKE import QKE
from receiver import Receiver
from transmitter import Transmitter

'''
Testing the QKE algorithm class via the Transmitter
and Receiver classes.

Created by Luke Finlayson, 1557835
'''

# Custom thread so we can get the key value from transmitter/receiver
class CustomThread(Thread):
    def __init__(self, target=None, args=()):
        Thread.__init__(self, target=target, args=args)
        self.key: list | None = None

    def run(self):
        if self._target is not None:
            self.key = self._target(*self._args)

def test_validPolarisation():
    # Generate some polarisations
    qke = QKE()
    qke.values            = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    qke.polarisations     = [0, 0, 1, 1, 0, 1, 0, 1, 1, 1]
    receivedPolarisations = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1]
    expectedKey           = [1, 1, 1, 1, 1]

    key = qke.createKey(receivedPolarisations)

    assert key == expectedKey

def test_otherPolarisation():
    # Generate some polarisations
    qke = QKE()
    qke.values            = [1, 1, 1, 1, 1, 1, 1, 1]
    qke.polarisations     = [0, 0, 1, 1, 0, 1, 0, 1]
    receivedPolarisations = [1, 1, 1, 1, 1, 1, 1, 1]
    expectedKey           = [1, 1, 1]

    key = qke.createKey(receivedPolarisations)

    assert key != expectedKey
    assert key != None

def test_emptyPolarisation():
    # Generate some polarisations
    qke = QKE()
    receivedPolarisations = []
    expectedMask          = []

    key = qke.createKey(receivedPolarisations)

    assert key == expectedMask

def test_keyExchange16():
    createKeys(16)

def test_keyExchange256():
    createKeys(256)

def test_keyExchange1024():
    createKeys(1024)

def createKeys(length: int):
    # Create several (thousand) keys to reduce randomness factor
    for i in range(1000):
        # Setup the receiver
      receiver = Receiver()
      port = receiver.open()

      assert port != None

      tThread = CustomThread(target=runTransmitter, args=(port, length))
      rThread = CustomThread(target=runReceiver, args=(receiver,))

      tThread.start()
      rThread.start()

      tThread.join()
      rThread.join()

      assert tThread.key == rThread.key
      assert len(tThread.key) != 0
      assert tThread.key != None

def runTransmitter(port: int, length: int):
    transmitter = Transmitter()
    transmitter.connect(port)
    
    transmitter.establishKey(length)
    transmitter.close()

    return transmitter.key

def runReceiver(receiver: Receiver):
    receiver.listen(receiver.establishKey)
    return receiver.key

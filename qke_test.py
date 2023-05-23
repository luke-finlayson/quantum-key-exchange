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
        self.value = None

    def run(self):
        if self._target is not None:
            self.value = self._target(*self._args)

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

def test_messageExchange16():
    exchangeMessages(["Hello, World!"], 16)

def test_messageExchange256():
    exchangeMessages(["Hello, World!"], 256)

def test_messageExchange1024():
    exchangeMessages(["Hello, World!"], 1024)

def test_messageExchange16Multiple():
    exchangeMessages(
        [
            "a", 
            "some extra long text that isnt really that long but kinda long at least longer than Hello, World!",
            "more text",
            "cow says moo",
            "this should be enough"
        ],
        16
    )

def test_messageExchange256Multiple():
    exchangeMessages(
        [
            "a", 
            "some extra long text that isnt really that long but kinda long at least longer than Hello, World!",
            "more text",
            "cow says moo",
            "this should be enough"
        ],
        256
    )

def test_messageExchange1024Multiple():
    exchangeMessages(
        [
            "a", 
            "some extra long text that isnt really that long but kinda long at least longer than Hello, World!",
            "more text",
            "cow says moo",
            "this should be enough"
        ],
        1024
    )

def exchangeMessages(messages: list, length: int):
    receiver = Receiver()
    port = receiver.open()

    assert port != None

    transmitter = Transmitter(port)

    # Establish the secret key
    tThread = CustomThread(target=transmitterGetKey, args=(transmitter, length))
    rThread = CustomThread(target=receiverGetKey, args=(receiver,))

    tThread.start()
    rThread.start()

    tThread.join()
    rThread.join()

    # Send the messages
    for message in messages:
        tThread = CustomThread(target=sendMessage, args=(transmitter, message))
        rThread = CustomThread(target=receiveMessage, args=(receiver,))

        rThread.start()
        tThread.start()

        rThread.join()
        tThread.join()

        assert rThread.value != None
        assert rThread.value == message

def createKeys(length: int):
    # Create several (thousand) keys to reduce randomness factor
    for i in range(500):
      # Arrange
      receiver = Receiver()
      port = receiver.open()

      assert port != None

      transmitter = Transmitter(port)

      tThread = CustomThread(target=transmitterGetKey, args=(transmitter, length))
      rThread = CustomThread(target=receiverGetKey, args=(receiver,))

      # Act
      tThread.start()
      rThread.start()

      tThread.join()
      rThread.join()

      # Assert
      assert tThread.value == rThread.value
      assert len(tThread.value) != 0
      assert tThread.value != None

def transmitterGetKey(transmitter: Transmitter, length: int):
    transmitter.establishKey(length)
    return transmitter.key

def sendMessage(transmitter: Transmitter, message: str):
    transmitter.sendMessage(message)
    return message

def receiverGetKey(receiver: Receiver):
    receiver.listen(receiver.establishKey)
    return receiver.key

def receiveMessage(receiver: Receiver):
    return receiver.listen(receiver.receive)
from threading import Thread
from receiver import Receiver
from transmitter import Transmitter

class CustomThread(Thread):
    def __init__(self, target=None, args=()):
        Thread.__init__(self, target=target, args=args)
        self.key = None

    def run(self):
        if self._target is not None:
            self.key = self._target(*self._args)

def createKeys(length: int):
    # Setup the receiver
    receiver = Receiver()
    port = receiver.open()

    if not port:
        return

    tThread = CustomThread(target=runTransmitter, args=(port, length))
    rThread = CustomThread(target=runReceiver, args=(receiver,))

    tThread.start()
    rThread.start()

    tThread.join()
    rThread.join()

    return tThread.key, rThread.key

def runTransmitter(port: int, length: int):
    transmitter = Transmitter()
    transmitter.connect(port)

    transmitter.establishKey(length)
    transmitter.close()

    return transmitter.key

def runReceiver(receiver: Receiver):
    receiver.listen(receiver.establishKey)
    return receiver.key

if __name__ == "__main__":
    for i in range(100):
        t, r = createKeys(16)
        print(t)

# Quantum Key Exchange

A simple transmitter and receiver that establish a secret key using an emulation of Quantum Key Exchange.
Subsequent messages can be sent once the key is established by using that key to encode and decode messages
with an XOR cipher.

## Usage

This project was created as a proof of concept - and while all the required functionality does exist, it is designed to be run via the unit tests.

However, the transmitter and receiver do include a simple main process so that they
can each be run as a standalone program in a command line interface. _Note that none of these command line interfaces include error handling_

- __Transmitter__: `python3 transmitter.py`
- __Receiver__: `python3 receiver.py`

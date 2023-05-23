import pytest
from Qubit import *

'''
Testing the emulation of a qubit
with the Qubit class.

Created by Luke Finlayson, 1557835
'''

def test_qubitMeasureValid():
    qubit = Qubit(0, 1)
    assert qubit.measure(1) == 0

def test_qubitMeasureInvalid():
    qubit = Qubit(0, 1)
    assert qubit.measure(0) == 0 or qubit.measure(0) == 1
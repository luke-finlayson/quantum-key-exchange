import pytest
from XOR import XOR

'''
Testing the XOR cipher class.
Expected encodings have been taken from https://dcode.fr.

Created by Luke Finlayson, 1557835
'''

def test_encodeRegularKey():
    xor = XOR(bytes([0,1,0,1,0,1,0,1]))
    phrase = "hello world!"
    
    expected = bytes([
        0b00111101,
        0b00110000,
        0b00111001,
        0b00111001,
        0b00111010,
        0b01110101,
        0b00100010,
        0b00111010,
        0b00100111,
        0b00111001,
        0b00110001,
        0b01110100
    ])

    assert xor.encode(phrase) == expected

def test_encodeSmallKey():
    xor = XOR(bytes([1,0,1]))
    phrase = "brown fox"
    
    expected = bytes([
        0b11010100,
        0b10101001,
        0b00000010,
        0b11000001,
        0b10110101,
        0b01001101,
        0b11010000,
        0b10110100,
        0b00010101
    ])

    assert xor.encode(phrase) == expected

def test_encodeLargeKey():
    xor = XOR(bytes([0,0,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1]))
    phrase = "a"

    expected = bytes([
        0b00111101
    ])

    assert xor.encode(phrase) == expected

def test_encodeDecodeMatch():
    xor = XOR(bytes([1,1,1,0,1,1,0,1]))
    phrase = "expected"

    encoded = xor.encode(phrase)
    assert xor.decode(encoded) == phrase

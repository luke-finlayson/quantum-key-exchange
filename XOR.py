from math import ceil

class XOR:
    '''
    Key is a binary value represented as an array
    of bytes - where each element is a single bit.

    Not very efficient space wise - but works for the purposes
    of this assignment
    '''
    def __init__(self, key: bytes):
      # Merge the bytes key into an int
      self.key = 0

      for i in key:
        self.key <<= 1
        self.key |= i

      self.keyLength = len(key)

    ''' 
    Creates a key for a given length in bytes
    made by repeating the stored key 
    '''
    def generateKey(self, length) -> bytes:
      numRepeats = ceil(length * 8) / self.keyLength
      result = 0
      
      for i in range(ceil(numRepeats)):
        result = result << self.keyLength
        result = result | self.key

      b = result.to_bytes(ceil(result.bit_length() / 8))
      return b[:length]
    
    '''
    Use the stored key to XOR a byte array
    '''
    def cipher(self, message: bytes) -> bytes:
      key = self.generateKey(len(message))

      # XOR the phrase with the key and return the encoded value
      return bytes([a ^ b for a, b in zip(message, key)]) 

    '''
    Encode a given string into a XOR ciphered byte array
    '''
    def encode(self, phrase: str) -> bytes:
      value = phrase.encode("utf-8");
      return self.cipher(value)
    
    '''
    Decode a given byte array into a string using the XOR cipher
    '''
    def decode(self, encoded: bytes) -> str:
       decoded = self.cipher(encoded)
       return decoded.decode("utf-8")

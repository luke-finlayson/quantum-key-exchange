from math import ceil

class XOR:
    def __init__(self, key: int, keyLength: int):
      self.key = key
      self.keyLength = keyLength

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
    def cipher(self, value: bytes) -> bytes:
      key = self.generateKey(len(value))

      # XOR the phrase with the key and return the encoded value
      return bytes([a ^ b for a, b in zip(value, key)]) 

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

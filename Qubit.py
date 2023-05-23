import random

class Qubit:
    def __init__(self, value, polarisation):
      self.value = value
      self.polarisation = polarisation
      
    def measure(self, polarisation):
      if (self.polarisation == polarisation):
        return self.value
      
      # Otherwise
      self.polarisation = polarisation
      self.value = random.randint(0, 1)
      
      return self.value
    
    @staticmethod
    def parse(s: str):
      values = s.split()
      values = [int(v) for v in values]

      return Qubit(values[0], values[1])
    

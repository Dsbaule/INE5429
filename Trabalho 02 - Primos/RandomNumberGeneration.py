import time

class LinearCongruentialGenerator:
    def __init__(self, seed=None, numMinBits = 32, m=None, a=1664525, c=1013904223, ):
        self.m = m if m is not None else 2**numMinBits # Módulo, 0 < m
        self.a = a  # Multiplicador, 0 < a < m
        self.c = c  # Incremento, 0 <= c < m
        self.numMinBits = numMinBits;

        # If no seed is provided, use time
        self.state = seed % self.m if seed is not None else int(time.time())

    def setMinBits(self, numMinBits):
        self.numMinBits = numMinBits
        self.m = 2 ** numMinBits

    # Generate next random number
    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        while self.state < (2**(self.numMinBits - 1)):
            self.state = (self.a * self.state + self.c) % self.m
        return self.state

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


class XorShiftGenerator:
    def __init__(self, seed=None):
        self.state = (seed & 0xffffffff if seed is not None else int(time.time()))

    def next(self):
        self.state ^= (self.state << 13) & 0xffffffff
        self.state ^= (self.state >> 17) & 0xffffffff
        self.state ^= (self.state << 5) & 0xffffffff
        return self.state

    def getNumber(self, numBits):
        # Make sure number has specified number of bits (Most significant bit 1)
        numBitsFirstNumber = numBits % 32
        next = 0
        if numBitsFirstNumber == 0:
            while next < 0x80000000:
                next = self.next()
            number = next
            numBits -= 32
        else:
            minNumber = 0x80000000 >> (32 - numBitsFirstNumber)
            maxNumber = 0x100000000 >> (32 - numBitsFirstNumber)
            while next < minNumber or next >= maxNumber:
                next = self.next()
            number = next
            numBits -= numBitsFirstNumber


        while numBits > 0:
            next = self.next()
            if numBits > 32:
                number = number << 32
                number |= next
                numBits -= 32
            else:
                number = number << numBits
                number |= (next & (0xffffffff >> (32 - numBits)))
                numBits = 0
        return number

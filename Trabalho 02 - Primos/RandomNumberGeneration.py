import time

'''
Linear Congruential Generation
From Wikipedia:
	def lcg(modulus, a, c, seed):
		while True:
			seed = (a * seed + c) % modulus
			yield seed
'''
class LinearCongruentialGenerator:
    def __init__(self, seed=None, numMinBits = 32, m=None, a=1664525, c=1013904223, ):
        self.m = m if m is not None else 2**numMinBits
        self.a = a
        self.c = c
        self.numMinBits = numMinBits;

        # If no seed is provided, use time
        self.state = seed % self.m if seed is not None else int(time.time())

	# Change bit count
    def setMinBits(self, numMinBits):
        self.numMinBits = numMinBits
        self.m = 2 ** numMinBits

    # Generate next random number
    def next(self):
		# Generate next number
        self.state = (self.a * self.state + self.c) % self.m
		# While number doesn't meet bit count requiremente, keep generating
        while self.state < (2**(self.numMinBits - 1)):
            self.state = (self.a * self.state + self.c) % self.m
		# Return random number
        return self.state

'''
Xorshift
From Wikipedia (C implementation):
	struct xorshift32_state {
	  uint32_t a;
	};

	/* The state word must be initialized to non-zero */
	uint32_t xorshift32(struct xorshift32_state *state)
	{
		/* Algorithm "xor" from p. 4 of Marsaglia, "Xorshift RNGs" */
		uint32_t x = state->a;
		x ^= x << 13;
		x ^= x >> 17;
		x ^= x << 5;
		return state->a = x;
	}
'''
class XorShiftGenerator:
	def __init__(self, seed=None):
		self.state = (seed & 0xffffffff if seed is not None else (int(time.time()) & 0xffffffff ))

	def next(self):
		self.state ^= (self.state << 13) & 0xffffffff
		self.state ^= (self.state >> 17) & 0xffffffff
		self.state ^= (self.state << 5) & 0xffffffff
		self.state &= 0xffffffff
		return self.state

	def getNumber(self, numBits):
		# Make sure number has specified number of bits (Most significant bit 1)
		numBitsFirstNumber = numBits % 32
		if numBitsFirstNumber == 0:
			numBitsFirstNumber = 32

		# Force number to have specified bit count
		next = self.next()
		number = next & (0xffffffff >> (32 - numBitsFirstNumber))
		number |= (0x80000000 >> (32 - numBitsFirstNumber))
		numBits -= numBitsFirstNumber

		# Concatenate remaining bits
		while numBits > 0:
			number = number << 32
			next = self.next()
			number |= next
			numBits -= 32

		return number

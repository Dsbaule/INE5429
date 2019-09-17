# Trabalho Individual 2 - Número Primos



## Números Aleatórios
## Números Primos
### Miller-Rabin
``` Python
from random import randint
'''
Miller-Rabin primality test
From wikipedia:
	Input #1: n > 3, an odd integer to be tested for primality
	Input #2: k, the number of rounds of testing to perform
	Output: “composite” if n is found to be composite,
    “probably prime” otherwise

	write n as 2^r·d + 1 with d odd (by factoring out powers of 2 from n − 1)
	WitnessLoop: repeat k times:
	   pick a random integer a in the range [2, n − 2]
	   x ← ad mod n
	   if x = 1 or x = n − 1 then
	      continue WitnessLoop
	   repeat r − 1 times:
	      x ← x^2 mod n
	      if x = n − 1 then
	         continue WitnessLoop
	   return “composite”
	return “probably prime”
'''
class MillerRabin:
	def decompose(n):
		r = 0
		while n % 2 == 0:
			r += 1
			n = n >> 1
		return r, n

	def testPrime(n, k=200):
		# Known small prime numbers
		if n in (2,3):
			return True
		# No number smaller than 2 is prime
		if n < 2:
			return False
		# No even number other than 2 is prime
		if n % 2 == 0:
			return False

		# Write n as 2^r·d + 1 with d odd (by factoring out powers of 2 from n − 1)
		r, d = MillerRabin.decompose(n - 1)

		# WitnessLoop: repeat k times:
		for _ in range(k):
			# Pick a random integer a in the range [2, n − 2]
			a = randint(2, n - 2)
			# x ← a^d mod n
			x = pow(a, d, n)
			# if x = 1 or x = n − 1 then continue WitnessLoop
			if x in (1, n - 1):
				continue
			try:
				# repeat r − 1 times:
				for _ in range(r - 1):
					# x ← x^2 mod n
					x = pow(x, 2, n)
					# if x = n − 1 then continue WitnessLoop
					if x == n - 1:
						raise Exeption()
			except Exception as e:
				continue

			return False
		return True
```
### Fermat
``` Python
from random import randint
'''
Fermat primality test
From wikipedia:
	Inputs: n: a value to test for primality, n>3; k: a parameter that
        determines the number of times to test for primality
	Output: composite if n is composite, otherwise probably prime
	Repeat k times:
		Pick a randomly in the range [2, n − 2]
		If a^(n-1) % n != 1, then return composite
		If composite is never returned: return probably prime
'''
class Fermat:
	def testPrime(n, k=200):
		# Known small prime numbers
		if n in (2, 3):
			return True
		# No number smaller than 2 is prime
		if n < 2:
			return False
		# No even number other than 2 is prime
		if n % 2 == 0:
			return False

		# Repeat k times:
		for _ in range(k):
			# Pick a randomly in the range [2, n − 2]
			a = randint(2, n - 2)
			# If a^(n-1) % n != 1, then return composite
			if pow(a, n - 1, n) != 1:
				return False
			# If composite is never returned: return probably prime
		return True
```

## Referências

Miller-Rabin

Fermat

Blum Blum Shub

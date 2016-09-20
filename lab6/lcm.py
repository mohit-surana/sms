'''
Linear Congruential Method
Author: doodhwala

Generate random numbers based on the three cases for LCM

'''

from fractions import gcd
from random import randint

def RandomGenerator(method, seed=0):
	a, m, c = 0, 0, 0
	if(method == 'Mixed'):
		# m = 2**b, c != 0, gcd(c,m) == 1, a = 1+4*k, P = m
		a = 17
		m = 8
		c = 43
	elif(method == 'Multiplicative-Pow2'):
		# m = 2**b, c = 0, a = 3+8*k or 5+8*k, P = m/4
		a = 29
		m = 16
		c = 0
	elif(method == 'Multiplicative-Prime'):
		# m = prime, c = 0, a = a**k - 1 is divisible by m (smallest value of k = m-1), P = (m-1)/2
		a = 2
		m = 11
		# Check if this selection is okay
		for k in range(1, m-1):
			if((int(a**k) - 1) % m == 0):
				raise StopIteration()
		if((int(a**(m-1)) - 1) % m != 0):
			raise StopIteration()
		c = 0
	elif(method == 'Multiplicative-Prime-Lab'):
		# m = prime, c = 0, a = a**k - 1 is divisible by m (smallest value of k = m-1), P = (m-1)/2
		a = int(7**5)
		m = (1<<31) - 1
		c = 0
	elif(method == 'Mixed-Rand'):
		# m = 2**b, c != 0, gcd(c,m) == 1, a = 1+4*k, P = m
		a = 1 + 4*randint(1,1<<32)
		m = 1<<32
		while(True):
			c = randint(1,1<<32)
			if(gcd(c,m) == 1):
				break
	elif(method == 'Multiplicative-Pow2-Rand'):
		# m = 2**b, c = 0, a = 3+8*k or 5+8*k, P = m/4
		a = 3 + 8*randint(1,1<<32)
		m = 1<<32
		c = 0
		seed = randint(1,1<<32)

	print(method, a, m, c, seed)
	N = 100
	while(N):
		x = (seed*a + c) % m
		r = x/m
		seed = x
		N -= 1
		yield r
	raise StopIteration()

gen1 = RandomGenerator('Mixed', 23)
gen2 = RandomGenerator('Multiplicative-Pow2', 1)
gen3 = RandomGenerator('Multiplicative-Prime', 7)
gen4 = RandomGenerator('Multiplicative-Prime-Lab', 123457)
gen5 = RandomGenerator('Mixed-Rand')
gen6 = RandomGenerator('Multiplicative-Pow2-Rand')

print(list(gen1)[:10], '\n')
print(list(gen2)[:10], '\n')
print(list(gen3)[:15], '\n')
print(list(gen4)[:10], '\n')
print(list(gen5)[:10], '\n')
print(list(gen6)[:10], '\n')

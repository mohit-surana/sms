'''
Linear Congruential Method
Author: doodhwala

Generate random numbers based on the three cases for LCM

'''

def RandomGenerator(method, seed):
	a, m, c = 0, 0, 0
	if(method == 'Mixed'):
		# m = 2**b, c != 0, gcd(c,m) == 1, a = 1+4*k, P = m
		a = 17	# 22695477
		m = 8	# 1<<32
		c = 43	# 1
	if(method == 'Mixed-C'):
		# m = 2**b, c != 0, gcd(c,m) == 1, a = 1+4*k, P = m
		a = 22695477
		m = 1<<32
		c = 1
	elif(method == 'Multiplicative-Pow2'):
		# m = 2**b, c = 0, a = 3+8*k or 5+8*k, P = m/4
		a = 29
		m = 16
		c = 0
	elif(method == 'Multiplicative-Prime'):
		# m = prime, c = 0, a = a**k - 1 is divisible by m (smallest value of k = m-1), P = (m-1)/2
		a = 2
		m = 23
		c = 0
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
gen4 = RandomGenerator('Mixed-C', 23)

print(list(gen1)[:10])
print(list(gen2)[:10])
print(list(gen3)[:15])
print(list(gen4)[:15])

'''
Random Number Generator
Author: doodhwala

Generate random numbers

'''

def RandomGenerator(seed=0, N=100):
	a = int(7**5)
	m = (1<<31) - 1
	c = 0
	while(N):
		x = (seed*a + c) % m
		r = x/m
		seed = x
		N -= 1
		yield r
	raise StopIteration()

rng = RandomGenerator(123457, 2000)
with open('random_numbers.txt', 'w') as f:
	f.write(' '.join([str(x) for x in rng]))

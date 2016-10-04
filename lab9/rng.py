'''
Random Number Generator
Author: doodhwala

Generate random numbers

'''

def RandomGenerator(seed=0, N=100):
	a = 1 + 4*int(input('Enter any value for k: '))
	m = 1<<23
	c = 1
	print('Using the values a =', a, 'm =', m, 'c =', c)
	while(N):
		x = (seed*a + c) % m
		r = x/m
		seed = x
		N -= 1
		yield r
	raise StopIteration()

rng = RandomGenerator(123457, 10000)
with open('random_numbers.txt', 'w') as f:
	f.write(' '.join([str(x) for x in rng]))
print('Generated 10000 random numbers')

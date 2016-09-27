'''
Random Number Generator
Author: doodhwala

Generate random numbers

'''

def RandomGenerator(method, seed=0, N=100):
	a, m, c = 0, 0, 0
	if(method == 0):
		a = int(7**5)
		m = (1<<31) - 1
		c = 0
	elif(method == 1):
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

# rng = RandomGenerator(0, 123457, 2000)
rng = RandomGenerator(1, 123457, 2000)
with open('random_numbers.txt', 'w') as f:
	f.write(' '.join([str(x) for x in rng]))
print('Generated 2000 random numbers')

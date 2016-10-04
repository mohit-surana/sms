'''
Random Variate Generator
Author: doodhwala

Generating random variates for Exponential, Uniform and Poisson distributions

'''

import math
import random

def RVG(method, maxN):
	numbers = []
	if(method == 'Exponential'):
		# Inverse transform method for Exponential
		# Xi =  -(1/lambda) * ln(R)
		l = float(input("Enter the value for lambda(l): "))
		for i in range(maxN):
			r = random.random()
			x = (-1/l) * math.log(r)
			numbers.append(x)

	elif(method == 'Uniform'):
		# Inverse transform method for Uniform Distribution
		# Xi =  (b - a) * R + a
		a, b = list(map(float, input("Enter the values for a and b: ").split()))
		for i in range(maxN):
			r = random.random()
			x = (b-a)*r + a
			numbers.append(x)
	elif(method == 'Poisson'):
		pass
	return numbers

if __name__ == '__main__':
	while(True):
		method = input("Enter the type of distribution (Exponential/Uniform/Poisson): ")
		maxN = int(input("How many numbers should be generated? "))
		random_variates = RVG(method, maxN)
		print(random_variates)

		with open(method + str(maxN), 'w') as f:
			f.write(' '.join([str(x) for x in random_variates]))

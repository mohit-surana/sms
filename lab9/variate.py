'''
Random Variate Generator
Author: doodhwala

Generating random variates for Exponential, Uniform and Poisson distributions

'''

import math

random_numbers = []
with open('random_numbers.txt', 'r') as f:
	random_numbers = [float(x) for x in f.read().split()]
index = 0

def RVG(method, maxN):
	global index
	numbers = []
	if(method == 'Exponential'):
		# Inverse transform method for Exponential
		# Xi =  -(1/lambda) * ln(R)
		l = float(input("Enter the value for lambda(l): "))
		for i in range(maxN):
			r = random_numbers[index]
			x = (-1/l) * math.log(r)
			numbers.append(x)
			index = (index + 1) % len(random_numbers)

	elif(method == 'Uniform'):
		# Inverse transform method for Uniform Distribution
		# Xi =  (b - a) * R + a
		a, b = list(map(float, input("Enter the values for a and b: ").split()))
		for i in range(maxN):
			r = random_numbers[index]
			x = (b-a)*r + a
			numbers.append(x)
			index = (index + 1) % len(random_numbers)
	elif(method == 'Poisson'):
		'''
			TODO: Complete this
		'''
		pass
	return numbers

if __name__ == '__main__':
	while(True):
		method = input("Enter the type of distribution (Exponential/Uniform/Poisson/Exit): ")
		if(method == 'Exit'):
			exit()
		maxN = int(input("How many numbers should be generated? "))
		random_variates = RVG(method, maxN)
		print(random_variates)

		with open(method + str(maxN), 'w') as f:
			f.write(' '.join([str(x) for x in random_variates]))

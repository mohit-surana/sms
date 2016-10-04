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
			index = (index + 1) % len(random_numbers)
			x = (-1/l) * math.log(r)
			numbers.append(x)

	elif(method == 'Uniform'):
		# Inverse transform method for Uniform Distribution
		# Xi =  (b - a) * R + a
		a, b = list(map(float, input("Enter the values for a and b: ").split()))
		for i in range(maxN):
			r = random_numbers[index]
			index = (index + 1) % len(random_numbers)
			x = (b-a)*r + a
			numbers.append(x)
	elif(method == 'Poisson'):
		# Acceptance rejection method
		# alpha is the value of the mean
		alpha = float(input("Enter the value for alpha: "))
		e_power_minus_alpha = math.exp(-alpha)
		for i in range(maxN):
			# Step 1
			n, p = 0, 1

			# Step 2
			while(True):
				r = random_numbers[index]
				index = (index + 1) % len(random_numbers)
				p = p * r
				if(p < e_power_minus_alpha):
					break
				n += 1
			numbers.append(n)
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

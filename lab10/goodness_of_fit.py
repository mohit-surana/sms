'''
Tests on Random Variates
Author: doodhwala

Apply Chi-Square test on the given variates

'''

import math

random_numbers = []

method = input("Enter the type of distribution (Exponential/Poisson/Exit): ")
if(method in ('Exponential', 'Poisson', 'Exit')):
	if(method == 'Exit'):
		exit()

	if(method == 'Exponential'):
		with open(method + '100', 'r') as f:
			random_numbers = [float(x) for x in f.read().split()]

	elif(method == 'Poisson'):
		with open(method + '100', 'r') as f:
			random_numbers = [int(x) for x in f.read().split()]

'''
Tests on Random Variates
Author: doodhwala

Apply Chi-Square test on the given variates

'''

import math
import sys
import csv

x0_table = { 0.05: { 1:3.84, 2:5.99, 3:7.81, 4:9.49, 5:11.1, 6:12.6, 7:14.1, 8:15.1 } }

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

	N = len(random_numbers)
	x_bar = sum(random_numbers)/N

	O = []
	E = []
	n = 10
	E_need = 5

	LHS = 1 # Normal LHS

	if(method == 'Exponential'):
		E_val = N/n
		# TODO: Fix this (E_val)
		for i in range(n):
			l = -x_bar * math.log(1 - i*(1/n))
			r = sys.maxsize if i==n-1 else -x_bar * math.log(1 - (i+1)*(1/n))
			E.append(E_val)
			O.append(len([x for x in random_numbers if l<=x<r]))

	elif(method == 'Poisson'):

		alpha = x_bar
		for i in range(n):
			p_i = math.exp(-alpha) * ( alpha**i) / math.factorial(i)
			E.append(N * p_i)
			O.append(random_numbers.count(i))

		# Proper method - don't use because it leads to k = 2 and degrees_of_freedom = 0 - undefined
		# Hence we let k = 4 (0, 1, 2, >=3)
		LHS = 4 # Shady LHS

	for i in range(LHS, n)[::-1]:
		if(E[i] < E_need):
			O[i-1] += O[i]
			E[i-1] += E[i]
			del O[i]
			del E[i]

	n = len(O)

	Oi_minus_Ei = [O[i] - E[i] for i in range(n)]
	Oi_minus_Ei_square = [x*x for x in Oi_minus_Ei]
	Oi_minus_Ei_square_by_Ei = [Oi_minus_Ei_square[i]/E[i] for i in range(n)]
	x0_sq = sum(Oi_minus_Ei_square_by_Ei)

	k, s = n, 1
	degrees_of_freedom = k-s-1
	x_table = x0_table[0.05][degrees_of_freedom]

	print('The value of x0 square is', x0_sq)
	print('The value of x0 square from the table is', x_table)

	if(x0_sq < x_table):
		print('We failed to reject the null hypothesis for uniformity for the given random numbers')
	else:
		print('Null hypothesis for Uniformity is rejected')

with open('simulation.csv', 'w', newline='') as csvfile:
    sheet = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    sheet.writerow(['i', 'O', 'E', 'Oi_minus_Ei', 'Oi_minus_Ei_square', 'Oi_minus_Ei_square_by_Ei'])
    for row in zip(list(range(n)), O, E, Oi_minus_Ei, Oi_minus_Ei_square, Oi_minus_Ei_square_by_Ei):
        sheet.writerow(row)

'''
Chi Square Test
Author: doodhwala

Uniformity Test - Chi Square

'''

random_numbers = []
with open('random_numbers.txt', 'r') as f:
	random_numbers = [float(x) for x in f.read().split()]

N = len(random_numbers)
n = 10

i = list(range(1, n+1))
Ri = random_numbers

O = []
for i in range(n):
	l, r = i*(1/n) , (i+1)*(1/n)
	O.append(len([x for x in Ri if l<=x<r]))

E = [N//n]*n
Oi_minus_Ei = [O[i] - E[i] for i in range(n)]
Oi_minus_Ei_square = [x*x for x in Oi_minus_Ei]

x0_sq = sum([Oi_minus_Ei_square[i]/E[i] for i in range(n)])

alpha = 0.5
x0_table = { (0.5, 9) : 16.9 }
print('The value of x0 square is', x0_sq)
print('The value of x0 square from the table is', x0_table[(alpha, n-1)])
if(x0_sq < x0_table[(alpha, n-1)]):
	print('Null hypothesis for Uniformity is accepted')
else:
	print('Null hypothesis for Uniformity is rejected')

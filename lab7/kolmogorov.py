'''
Kolmogorov - Smirnov Test
Author: doodhwala

Uniformity Test - Kolmogorov Smirnov

'''

random_numbers = []
with open('random_numbers.txt', 'r') as f:
	random_numbers = [float(x) for x in f.read().split()]

N = 50

i = list(range(1, N+1))
Ri = random_numbers[:N]
Ri.sort()
i_by_N = [x/N for x in i]
i_by_N_minus_Ri = [i_by_N[x] - Ri[x] for x in range(N)]

# Need to append to the left because i_by_N[-1] won't give us what we want
Ri_minus_i_minus_1_by_N = [Ri[0]] + [Ri[x] - i_by_N[x-1] for x in range(1,N)]

D_plus = max(i_by_N_minus_Ri)
D_minus = max(Ri_minus_i_minus_1_by_N)
D = max(D_plus, D_minus)

D_table = { 0.05 : 0.565 }
print('The value of D is', D)
if(D < D_table[0.05]):
	print('Null hypothesis for Uniformity is accepted')
else:
	print('Null hypothesis for Uniformity is rejected')

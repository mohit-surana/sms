'''
Autocorrelation Test
Author: doodhwala

Independence Test - Autocorrelation Test

'''

random_numbers = []
with open('random_numbers.txt', 'r') as f:
	random_numbers = [float(x) for x in f.read().split()]

N = int(input('Enter the value for N: '))
i = int(input('Enter the value for i: '))
m = int(input('Enter the value for m: '))

# i + (M+1)m <= N
M = (N-i)//m - 1

print('N={}, i={}, m={}, M={}'.format(N, i, m, M))

'''
rho_im_cap = (1/(M+1)) * ( Total of R[i+km] x R[i+(k+1)m] ) - 0.25
sigma_rho_im_cap = sqrt(13*M + 7) / 12(M+1)
Z = rho_im_cap / sigma_rho_im_cap
'''

R = random_numbers
total = 0
for k in range(M+1):
	total += R[i+k*m] * R[i+(k+1)*m]

rho_im_cap = total/(M+1) - 0.25
sigma_rho_im_cap = ((13*M + 7) ** 0.5) / (12*(M+1))
Z = rho_im_cap / sigma_rho_im_cap

alpha = 0.05
Z_table = { alpha/2: 1.96 }
print('The value of Z is', Z)
print('The value of Z_table is', Z_table[alpha/2])
if(-Z_table[alpha/2] <= Z <= Z_table[alpha/2]):
	print('We failed to reject the null hypothesis for uniformity for the given random numbers')
else:
	print('Null hypothesis for Uniformity is rejected')

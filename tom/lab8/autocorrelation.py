from rng import RandomGenerator
from random import randint

# random numbers
r = list(RandomGenerator(0))
#r = [0.32, 0.1, 0.23, 0.28, 0.89, 0.31, 0.64, 0.28, 0.83, 0.93, 0.99, 0.15, 0.33, 0.35, 0.91, 0.41, 0.6, 0.27, 0.75, 0.88, 0.68, 0.49, 0.05, 0.43, 0.95, 0.58, 0.19, 0.36, 0.69, 0.87]
z_alpha = 1.96

N = len(r)
i = randint(1, N)
m = randint(1, N)
#i, m = 1, 4

i -= 1
M = (N - i)//m - 1

if M < 0:
	print("Can't perform test!")
	exit()

rho = 0
for k in range(M+1):
	rho += r[i+k*m] * r[i+(k+1)*m]
rho /= (M+1)
rho -= 0.25

sigma = (13*M + 7)**0.5/(12*(M+1))

z = rho/sigma
print('M: %d, rho: %f, sigma: %f, z: %f' % (M, rho, sigma, z))

if -z_alpha < z and z < z_alpha:
	print("Null hypothesis is accpeted")
else:
	print("Null hypothesis is rejected")
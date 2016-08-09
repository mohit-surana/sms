#!/usr/bin/python3
import random
import matplotlib.pyplot as plt

Xb = [80, 90, 99, 108, 116, 125, 133, 141, 151, 160, 169, 179, 180]
Yb = [0, -2, -5, -9, -15, -18, -23, -29, -28, -25, -21, -20, -17]

xi = random.randint(0, 60)
yi = random.randint(0, 60)
# xi, yi = 0, 50
print('Initial Position -> (', xi, ', ', yi, ')', sep='')

Xf = [xi]
Yf = [yi]

Vf = 20
hit = False
t = 0

for t in range(12):
	dist = ( (Yb[t] - Yf[t]) ** 2 + (Xb[t] - Xf[t]) ** 2 ) ** 0.5
	if(dist <= 10):
		hit = True
		break
	sin = ( Yb[t] - Yf[t] ) / dist
	cos = ( Xb[t] - Xf[t] ) / dist
	Xf.append(Xf[t] + Vf*cos)
	Yf.append(Yf[t] + Vf*sin)

if(t == 11):
	t += 1
	dist = ( (Yb[t] - Yf[t]) ** 2 + (Xb[t] - Xf[t]) ** 2 ) ** 0.5
	print(t, dist)

if(hit):
	print('Success')
	print('Hit the bomber plane at t =', t-1)
else:
	print('Miss')

n = t+1

'''
# 2D plot
plt.plot(Xb[:n], Yb[:n], 'r:')
plt.plot(Xb[:n], Yb[:n], 'ro')
plt.plot(Xf, Yf, 'b--')
plt.plot(Xf, Yf, 'bo')
plt.show()
'''

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ts = list(range(n))

ax.scatter(Xf, ts, Yf, marker='o', c='r')
ax.scatter(Xb[:n], ts, Yb[:n], marker='^', c='b')
ax.set_xlabel('X')
ax.set_zlabel('Y')
ax.set_ylabel('T')
plt.show()

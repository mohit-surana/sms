'''
Alternate solution
Author: Shiva Deviah (https://github.com/Coldsp33d)

'''

import math
import random
import matplotlib.pyplot as plt #sudo apt-get install python matplotlib
import time


Vf = 20

B = [(80, 0), (90, -2), (99, -5), (108, -9), (116, -15), (125, -18), (133, -23), (141, -29), (151, -28), (160, -25), (169, -21), (179, -20), (180, -17)]

(Xf, Yf) = (random.random() * 50, random.random() * 50)
plt.plot([], [])
plt.ion()

print "Initial coordinates: ({:.2f}, {:.2f})".format(Xf, Yf)
print "Figher velocity: ", Vf
print 

for i, coord in enumerate(B):
	plt.clf()
	plt.plot([coord[0], Xf], [coord[1], Yf], "ro") 
	plt.axis([-50, 150, -50, 50])
	plt.annotate('Fighter', xy=(Xf, Yf)) 
	plt.annotate('Bomber', xy=coord) 
	plt.pause(1)
	print "Minute {}: Fighter({:.2f}, {:.2f}), Bomber{}".format(i, Xf, Yf, coord)
	Dt = float( (( coord[1] - Yf) ** 2 ) +  (( coord[0] - Xf) ** 2 ) )  ** 0.5
	print "\t\t\t\t\tDistance: {:.2f}".format(Dt)
	if Dt <= 10: 
		print 'Simulation successful'
		while True:
			plt.pause(10000)
		exit()
		
	sin_theta = float(coord[1] - Yf) / Dt
	cos_theta = float(coord[0] - Xf) / Dt
	
	Xf = Xf + Vf * cos_theta
	Yf = Yf + Vf * sin_theta
	
print 'Unsuccessful simulation'

while True:
	plt.pause(10000)


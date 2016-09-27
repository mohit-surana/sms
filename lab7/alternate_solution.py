'''
Alternate solution
Author: Shiva Deviah (https://github.com/Coldsp33d)

'''

import numpy as np
import random
import os

def kolmogorov_smirnov(R, verbose=False):
	N = len(R)
	R1 = sorted(R)

	dAlpha005 = 1.36 / np.sqrt(N)

	i = (np.arange(len(R)) + 1).astype(np.float64)

	dPlus = np.max(( i / len(R) ) - R1)
	dMinus = np.max(R1 - ( ( i - 1).astype(np.float64) / N ))

	if verbose:
		print "D+: {:.4f}\tD-: {:.4f}".format(dPlus, dMinus)
		print "D : {:.4f}\tDa: {:.4f}".format(max(dPlus, dMinus), dAlpha005)

	if max(dPlus, dMinus) <= dAlpha005:
		return True

	return False

def chi_squared(R, num_intervals=10, verbose=False):
	Xsq005_LIST = [3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307, 19.675, 21.026, 22.362, 23.685, 24.996, 26.296, 27.587, 28.869, 30.144, 31.410, 32.671, 33.924, 35.172, 36.415, 37.652, 38.885, 40.113, 41.337, 42.557, 43.773, 44.985, 46.194, 47.400, 48.602, 49.802, 50.998, 52.192, 53.384, 54.572, 55.758, 56.942, 58.124, 59.304, 60.481, 61.656, 62.830, 64.001, 65.171, 66.339, 67.505, 68.669, 69.832, 70.993, 72.153, 73.311, 74.468, 75.624, 76.778, 77.931, 79.082, 80.232, 81.381, 82.529, 83.675, 84.821, 85.965, 87.108, 88.250, 89.391, 90.531, 91.670, 92.808, 93.945, 95.081, 96.217, 97.351, 98.484, 99.617, 100.749, 101.879, 103.010, 104.139, 105.267, 106.395, 107.522, 108.648, 109.773, 110.898, 112.022, 113.145, 114.268, 115.390, 116.511, 117.632, 118.752, 119.871, 120.990, 122.108, 123.225, 124.342, 124.342]

	num_intervals += len(R) % num_intervals

	Xsq005 = Xsq005_LIST[num_intervals - 2]

	intervals = [(float(i) / 100.0, float(i + 100 // num_intervals)/ 100.0) for i in range(0, 100, 100 // num_intervals)]

	Oi = np.zeros(num_intervals)

	Ei = float(len(R)) / num_intervals

	for num in R:
		for i, t  in enumerate(intervals):
		 	if t[0] <= num < t[1]:
				Oi[i] += 1
				break

	Xsq = np.sum(  ( ( Oi - Ei ) ** 2) / Ei )

	if verbose:
		print "Xsq0: {:.4f}\tXsq005: {:.4f}".format(Xsq, Xsq005)

	if Xsq <= Xsq005:
		return  True

	return False


if __name__ == "__main__":
	np.random.seed(os.getpid())

	SIZE = 50
	R = np.random.uniform(low=0.0, high=1.0, size=SIZE)

	print "Running K - S test"

	if(kolmogorov_smirnov(R, True)):
		print "Null hypothesis accepted"
	else:
		print "Null hypothesis rejected"

	SIZE = 10000
	NUM_INTERVALS = 50
	R = np.random.uniform(low=0.0, high=1.0, size=SIZE)

	print "\nRunning Chi-Squared test"

	if(chi_squared(R, NUM_INTERVALS, True)):
		print "Null hypothesis accepted"
	else:
		print "Null hypothesis rejected"

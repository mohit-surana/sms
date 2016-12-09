# Disclaimer

There are a lot of random stuff in the code

These are the main concepts:

Linear Congruential Method

	X(i+1) = a*X(i) + c % m
	
	if(method == 'Mixed'):
		m = 2**b, c != 0, gcd(c,m) == 1, a = 1+4*k, P = m
		
	elif(method == 'Multiplicative-Pow2'):
		m = 2**b, c = 0, a = 3+8*k or 5+8*k, P = m/4
		
	elif(method == 'Multiplicative-Prime'):
		m = prime, c = 0, a = a**k - 1 is divisible by m (smallest value of k = m-1), P = (m-1)/2
		

	

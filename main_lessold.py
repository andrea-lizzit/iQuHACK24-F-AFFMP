import numpy as np
from math import comb, factorial
from itertools import combinations_with_replacement
from itertools import permutations

def factl(l):
	return [factorial(i) for i in l]

def permanent(matrix):
    n = len(matrix)
    perm_sum = 0

    for perm in permutations(range(n)):
        product = 1
        for i in range(n):
            product *= matrix[i, perm[i]]
        perm_sum += product

    return perm_sum

def A(lam):
	N = lam.shape[0]
	n = 2
	N_out = comb(N+n-1, n)
	for comb_n in combinations_with_replacement(range(N), n):
		for comb_m in combinations_with_replacement(range(N), n):
			omega = np.zeros(N)
			for x in comb_n:
				omega[x] += 1
			
			omegap = np.zeros(N)
			for x in comb_m:
				omegap[x] += 1

			sub = lam[omegap, omega]
			prefactor = np.sqrt(factl(omega).prod() * factl(omegap).prod())
			return prefactor * permanent(sub)
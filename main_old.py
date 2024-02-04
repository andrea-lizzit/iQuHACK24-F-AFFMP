import numpy as np
from math import comb
from itertools import combinations_with_replacement

def index_of_fock_state(N, n, v):
	v = np.array(v)
	i = 0
	for c in combinations_with_replacement(range(N), n):
		if np.all(np.array(c) == v):
			return i
		i += 1
	
	
def A(U):
	N = U.shape[0]
	n = 2
	N_out = comb(N+n-1, n)
	out = np.ones((N_out, n))
	out *= 42
	for special_i in range(N_out):
		
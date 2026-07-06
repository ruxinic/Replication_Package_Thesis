import numpy as np

def primes_upto(limit):
    # G24: replace the native list with a high-performance NumPy boolean array
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    
    # calculate the termination boundary
    loop_bound = int(limit**0.5 + 1.5)
    
    for n in range(loop_bound):
        if is_prime[n]:
            # G24: leverage NumPy's high-performance sliced array assignment 
            # to clear composite numbers efficiently
            is_prime[n*n : limit+1 : n] = False
            
    # use NumPy's optimized nonzero evaluation to extract the prime indices
    return np.nonzero(is_prime)[0].tolist()

primes_upto(100000000)
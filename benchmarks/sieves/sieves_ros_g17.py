import math

def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    # G17: avoid calling heavy math operations or library functions inside loop declarations
    # calculate the square root once outside the loop
    computed_boundary = int(math.sqrt(limit) + 1.5)
    
    for n in range(computed_boundary): 
        if is_prime[n]:
            for i in range(n*n, limit+1, n):
                is_prime[i] = False
                
    return [i for i, prime in enumerate(is_prime) if prime]

primes_upto(100000000)
from functools import lru_cache

# G18: add @lru_cache
@lru_cache(maxsize=128)
def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    for n in range(int(limit**0.5 + 1.5)): # stop at ``sqrt(limit)``
        if is_prime[n]:
            for i in range(n*n, limit+1, n):
                is_prime[i] = False
                
    return [i for i, prime in enumerate(is_prime) if prime]

# First call: Executes the full algorithm and caches the result
primes_upto(100000000)
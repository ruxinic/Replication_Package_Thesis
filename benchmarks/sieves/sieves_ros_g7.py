def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    for n in range(int(limit**0.5 + 1.5)): # stop at ``sqrt(limit)``
        if is_prime[n]:
            # G7: apply bulk operations using list slicing to update 
            # a batch of elements at once instead of one by one
            is_prime[n*n : limit+1 : n] = [False] * len(range(n*n, limit+1, n))
            
    return [i for i, prime in enumerate(is_prime) if prime]

primes_upto(100000000)
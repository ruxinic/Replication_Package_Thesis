def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    for n in range(int(limit**0.5 + 1.5)): 
        if is_prime[n]:
            for i in range(n*n, limit+1, n):
                # G6: avoid saving/storing data that is already computed
                # only write False if it hasn't been set yet
                if is_prime[i]: 
                    is_prime[i] = False
                
    return [i for i, prime in enumerate(is_prime) if prime]

primes_upto(100000000)
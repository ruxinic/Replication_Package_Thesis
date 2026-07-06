def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    for n in range(int(limit**0.5 + 1.5)): 
        if is_prime[n]:
            # G28: minimize individual memory accesses by aggregating the 
            # mutations into a single block slice assignment operation
            # instead of executing a loop of writes, write the entire batch at once
            is_prime[n*n : limit+1 : n] = [False] * len(range(n*n, limit+1, n))
                
    return [i for i, prime in enumerate(is_prime) if prime]

primes_upto(100000000)
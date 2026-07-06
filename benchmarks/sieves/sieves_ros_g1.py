def primes_upto(limit):
    # G1: assign 'limit + 1' to a variable 
    array_size = limit + 1  
    is_prime = [False] * 2 + [True] * (array_size - 2) 
    
    # G1: extract the loop bound expression into a variable
    loop_bound = int(limit**0.5 + 1.5)
    
    for n in range(loop_bound): # stop at ``sqrt(limit)``
        if is_prime[n]:
            # G1: use 'array_size' instead of repeating 'limit + 1'
            for i in range(n * n, array_size, n):
                is_prime[i] = False
                
    return [i for i, prime in enumerate(is_prime) if prime]

primes_upto(100000000)
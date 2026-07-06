def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    
    # G3: store the loop end condition in a variable 
    outer_loop_end = int(limit**0.5 + 1.5)
    
    for n in range(outer_loop_end): # stop at ``sqrt(limit)``
        if is_prime[n]:
            # G3: store the inner loop's end condition 
            # in a variable before execution.
            inner_loop_end = limit + 1
            
            for i in range(n*n, inner_loop_end, n):
                is_prime[i] = False
                
    return [i for i, prime in enumerate(is_prime) if prime]

primes_upto(100000000)
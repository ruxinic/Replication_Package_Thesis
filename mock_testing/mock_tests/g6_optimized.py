import math

def expensive_calculation(n):
    return sum(math.factorial(i % 10) for i in range(n))

def process_g6_optimized(n):
    # G6: Store data in a local variable to avoid recomputation
    cached_val = expensive_calculation(n)
    
    result_plus_one = cached_val + 1
    result_squared = cached_val ** 2
    result_str = str(cached_val)
    
    return result_plus_one, result_squared, result_str

process_g6_optimized(100000)
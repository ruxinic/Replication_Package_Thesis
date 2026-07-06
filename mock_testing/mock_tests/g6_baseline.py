import math

def expensive_calculation(n):
    # Simulate a heavy task
    return sum(math.factorial(i % 10) for i in range(n))

def process_g6_baseline(n):
    # Recomputing the same data three times unnecessarily
    result_plus_one = expensive_calculation(n) + 1
    result_squared = expensive_calculation(n) ** 2
    result_str = str(expensive_calculation(n))
    
    return result_plus_one, result_squared, result_str

process_g6_baseline(100000)
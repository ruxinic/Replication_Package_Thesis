from functools import lru_cache

@lru_cache(maxsize=None)
def fib_optimized(n):
    if n <= 1:
        return n
    # Result is retrieved from cache if it exists
    return fib_optimized(n - 1) + fib_optimized(n - 2)

print(fib_optimized(35)) # Instantaneous
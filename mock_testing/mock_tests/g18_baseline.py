def fib(n):
    if n <= 1:
        return n
    # No memory of previous results
    # Every branch recalculates everything from scratch
    return fib(n - 1) + fib(n - 2)

print(fib(35))
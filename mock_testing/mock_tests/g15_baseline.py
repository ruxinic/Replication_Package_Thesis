import time

def calculate_sum_baseline(n):
    total = 0.0
    for i in range(n):
        # Heavy mathematical operation in pure Python
        total += (i ** 0.5) * (i ** 1.5)
    return total

# Run a heavy loop
calculate_sum_baseline(20_000_000)
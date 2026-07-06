import math

# G5: Approximate calculation using standard float hardware
def calculate_sqrt_optimized(n):
    total = 0.0
    for i in range(1, n + 1):
        # Using standard hardware-accelerated square root
        total += math.sqrt(i)
    return total

calculate_sqrt_optimized(1000000)
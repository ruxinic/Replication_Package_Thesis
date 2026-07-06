from numba import njit

# G15: Use a compiled language/JIT for performance-critical sections
@njit
def calculate_sum_optimized(n):
    total = 0.0
    for i in range(n):
        # This loop now runs as compiled machine code (speed of C)
        total += (i ** 0.5) * (i ** 1.5)
    return total

# Run the same heavy loop
calculate_sum_optimized(20_000_000)
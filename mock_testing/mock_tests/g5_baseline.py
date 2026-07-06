import math
from decimal import Decimal, getcontext

# High-precision square root summation
def calculate_sqrt_baseline(n):
    getcontext().prec = 50  # 50 decimal places
    total = Decimal(0)
    for i in range(1, n + 1):
        # Calculating high-precision square root
        total += Decimal(i).sqrt()
    return total

calculate_sqrt_baseline(1000000)
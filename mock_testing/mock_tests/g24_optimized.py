import numpy as np
import random

# Create two 500x500 matrices using NumPy arrays
size = 500
A_np = np.random.rand(size, size)
B_np = np.random.rand(size, size)

def run_optimized():
    # NumPy uses optimized BLAS libraries under the hood
    return np.matmul(A_np, B_np)

if __name__ == "__main__":
    run_optimized()

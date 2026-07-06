import random

# Create two 500x500 matrices using standard Python lists
# (We use 500 instead of 1000 because pure Python is VERY slow here)
size = 500
A = [[random.random() for _ in range(size)] for _ in range(size)]
B = [[random.random() for _ in range(size)] for _ in range(size)]
C = [[0 for _ in range(size)] for _ in range(size)]

def run_baseline():
    # Standard O(n^3) matrix multiplication in pure Python
    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i][j] += A[i][k] * B[k][j]
    return C

if __name__ == "__main__":
    run_baseline()

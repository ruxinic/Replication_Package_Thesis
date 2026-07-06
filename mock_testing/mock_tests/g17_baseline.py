import numpy as np

# Setup: 100,000 vectors of size 3
data = np.random.rand(100000, 3)
magnitudes = []

# Repeatedly calling a heavy library function in a loop
for vector in data:
    m = np.linalg.norm(vector)  # High overhead per iteration
    magnitudes.append(m)
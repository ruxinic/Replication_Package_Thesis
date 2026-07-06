import numpy as np

def generate_data_optimized(n):
    # G7: Use bulk operations to generate a batch at once
    # This reduces the overhead of handling individual tasks
    data = np.random.randint(1, 101, size=n)
    return data

generate_data_optimized(1000000)
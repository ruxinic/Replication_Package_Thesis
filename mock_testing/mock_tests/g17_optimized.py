import numpy as np

# Setup: Same 100,000 vectors
data = np.random.rand(100000, 3)

# Call the function once on the entire array
# The 'axis=1' tells NumPy to calculate the norm across the columns
magnitudes = np.linalg.norm(data, axis=1)
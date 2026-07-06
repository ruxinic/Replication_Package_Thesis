import sys
import random
import numpy as np
# Source: Rosetta Code (Sorting algorithms/Bubble sort)

def run_benchmark(data):
    arr = np.array(data)
    filtered = arr[arr % 2 == 0] # Vectorized filtering
    return np.sort(filtered)      # Optimized library sort

#ADDED:
if __name__ == "__main__":
    # N-value from the bash script (e.g., 2000)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    random.seed(42)
    
    # Generate input data
    input_data = [random.randint(1, 1000) for _ in range(N)]
    
    result = run_benchmark(input_data)
    
    print(f"Items sorted: {len(result)}")
    print(f"Checksum: {sum(result)}")
import sys
import random
# Source: Rosetta Code (Sorting algorithms/Bubble sort)

def bubble_sort_g2(seq):
    n = len(seq)
    while n > 1:
        new_n = 0
        for i in range(n - 1):
            if seq[i] > seq[i+1]:
                seq[i], seq[i+1] = seq[i+1], seq[i]
                # G2: track the last swap position; elements beyond this point are already sorted.
                new_n = i + 1 
        # update n to the last swap position to avoid redundant checks
        n = new_n 
    return seq

def run_benchmark(data):
    filtered_data = []
    for x in data:
        if x % 2 == 0:
            filtered_data.append(x)
            
    return bubble_sort_g2(filtered_data)
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
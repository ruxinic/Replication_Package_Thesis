import sys
import random
# Source: Rosetta Code (Sorting algorithms/Bubble sort)

def bubble_sort_g1(seq):
    changed = True
    while changed:
        changed = False
        for i in range(len(seq) - 1):
            # G1: save seq[i + 1] into a variable to reuse
            val = seq[i + 1]
            if seq[i] > val:
                seq[i], seq[i+1] = seq[i+1], seq[i]
                changed = True
    return seq

def run_benchmark(data):
    filtered_data = []
    for x in data:
        if x % 2 == 0:
            filtered_data.append(x)
            
    return bubble_sort_g1(filtered_data)
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
import sys
import random
# Source: Rosetta Code (Sorting algorithms/Bubble sort)

def run_benchmark(data):
    filtered_data = []
    for x in data:
        if x % 2 == 0:
            filtered_data.append(x)
    changed = True
    while changed:
        changed = False
        # G19: inline the sorting logic
        for i in range(len(filtered_data) - 1):
            if filtered_data[i] > filtered_data[i+1]:
                filtered_data[i], filtered_data[i+1] = filtered_data[i+1], filtered_data[i]
                changed = True
    return filtered_data
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
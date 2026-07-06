import ctypes
import os
import sys
import random
import numpy as np

lib_path = os.path.abspath("./bs_lib.so")
_lib = ctypes.CDLL(lib_path)

# Bind function signatures: void compute_bubble_sort(long long* arr, int size)
_lib.compute_bubble_sort.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.int64, ndim=1, flags='C_CONTIGUOUS'),
    ctypes.c_int
]
_lib.compute_bubble_sort.restype = None

def run_benchmark_g8(data):
    filtered_list = [x for x in data if x % 2 == 0]
    # Cast to an optimized 64-bit hardware array structure
    filtered_data = np.array(filtered_list, dtype=np.int64)
    size = len(filtered_data)
    # Delegate the heavy sorting straight to C
    if size > 0:
        _lib.compute_bubble_sort(filtered_data, size)
    return filtered_data
#ADDED:
if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    random.seed(42)
    
    # Generate identical underlying input datasets 
    input_data = [random.randint(1, 1000) for _ in range(N)]
    
    result = run_benchmark_g8(input_data)
    
    print(f"Items sorted: {len(result)}")
    print(f"Checksum: {int(result.sum())}")
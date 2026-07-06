from itertools import repeat
from math import sqrt
from multiprocessing import Pool
from sys import argv

def eval_A(i, j):
    ij = i + j
    return 1.0 / (ij * (ij + 1) / 2 + i + 1)

# G7: bulk Processing Function
def compute_chunk(u, indices):
    # compute a bulk set of sums for a range of indices.
    results = []
    local_eval = eval_A
    u_len = len(u)
    for i in indices:
        x = 0
        for j in range(u_len):
            x += local_eval(i, j) * u[j]
        results.append(x)
    return results

# G7: alternative bulk function for transpose
def compute_chunk_t(u, indices):
    results = []
    local_eval = eval_A
    u_len = len(u)
    for i in indices:
        x = 0
        for j in range(u_len):
            x += local_eval(j, i) * u[j]
        results.append(x)
    return results

def multiply_AtAv(u, pool, n, chunk_size):
    # G7: partition the indices into bulk chunks
    chunks = [range(i, min(i + chunk_size, n)) for i in range(0, n, chunk_size)]
    
    # send bulk chunks to workers
    tmp_nested = pool.starmap(compute_chunk, zip(repeat(u), chunks))
    # flatten the results
    tmp = [item for sublist in tmp_nested for item in sublist]
    
    v_nested = pool.starmap(compute_chunk_t, zip(repeat(tmp), chunks))
    return [item for sublist in v_nested for item in sublist]

def main():
    n = int(argv[1])
    u = [1.0] * n
    # define a chunk size for bulk operations
    chunk_size = max(1, n // 8) 

    with Pool(processes=4) as pool:
        for _ in range(10):
            v = multiply_AtAv(u, pool, n, chunk_size)
            u = multiply_AtAv(v, pool, n, chunk_size)

        vBv = vv = 0.0
        for i in range(n):
            vBv += u[i] * v[i]
            vv  += v[i] * v[i]

        print("{0:.9f}".format(sqrt(vBv / vv)))

if __name__ == '__main__':
    main()
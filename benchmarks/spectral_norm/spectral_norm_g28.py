from itertools import repeat
from math import sqrt
from multiprocessing import Pool
from sys import argv

# G28: chunk operations to process localized mathematical arrays
def eval_A_block(args):
    # process an entire contiguous range of rows in a single memory layout
    u, start_row, end_row = args
    results = []
    
    # cache global lookups inside the local block memory scope
    len_u = len(u)
    for i in range(start_row, end_row):
        x = 0.0
        # aggregating operations sequentially allows the CPU/interpreter 
        # to read u_j from contiguous caches
        for j in range(len_u):
            ij = i + j
            x += u[j] / (ij * (ij + 1) / 2 + i + 1)
        results.append(x)
    return results


def eval_At_block(args):
    # process an entire contiguous range of rows for the transposed matrix multiplication
    u, start_row, end_row = args
    results = []
    len_u = len(u)
    
    for i in range(start_row, end_row):
        x = 0.0
        for j in range(len_u):
            # G28: eval_A(j, i) inline
            ji = j + i
            x += u[j] / (ji * (ji + 1) / 2 + j + 1)
        results.append(x)
    return results


def multiply_AtAv(u, pool, num_workers):
    n = len(u)
    # determine coarse-grained block sizes to minimize process-switching I/O calls
    chunk_size = (n + num_workers - 1) // num_workers
    
    # G28: bundle row boundary allocations upfront
    tasks_A = []
    for w in range(num_workers):
        start = w * chunk_size
        end = min(start + chunk_size, n)
        if start < end:
            tasks_A.append((u, start, end))

    # single parallel blast map processes fetch vast blocks at once
    chunks_tmp = pool.map(eval_A_block, tasks_A)
    
    # flatten the retrieved contiguous results with fast list extension
    tmp = []
    for chunk in chunks_tmp:
        tmp.extend(chunk)
        
    # repackage task parameters for the transpose calculation pass
    tasks_At = []
    for w in range(num_workers):
        start = w * chunk_size
        end = min(start + chunk_size, n)
        if start < end:
            tasks_At.append((tmp, start, end))

    chunks_res = pool.map(eval_At_block, tasks_At)
    
    res = []
    for chunk in chunks_res:
        res.extend(chunk)
        
    return res


def main():
    n = int(argv[1]) if len(argv) > 1 else 100
    u = [1.0] * n
    
    num_workers = 4

    with Pool(processes=num_workers) as pool:
        for _ in range(10):
            v = multiply_AtAv(u, pool, num_workers)
            u = multiply_AtAv(v, pool, num_workers)

        vBv = 0.0
        vv = 0.0

        for ue, ve in zip(u, v):
            vBv += ue * ve
            vv  += ve * ve

        result = sqrt(vBv / vv)
        print("{0:.9f}".format(result))


if __name__ == '__main__':
    main()
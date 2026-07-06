from math import sqrt
from multiprocessing import Pool
from sys import argv

# G18: the expensive function is only called once per coordinate
def eval_A(i, j):
    ij = i + j
    return 1.0 / (ij * (ij + 1) / 2 + i + 1)

# G18: global memoization matrix
memo_matrix = []

def init_worker(matrix):
    global memo_matrix
    memo_matrix = matrix


def A_sum(u, i):
    x = 0.0
    # G18: access the pre-calculated "memo" row instead of calling eval_A
    row = memo_matrix[i]
    for j, u_j in enumerate(u):
        x += row[j] * u_j
    return x

def At_sum(u, i):
    x = 0.0
    # G18: access the pre-calculated "memo" for transpose lookup
    for j, u_j in enumerate(u):
        x += memo_matrix[j][i] * u_j
    return x

def multiply_AtAv(u, pool, n):
    r = range(n)
    
    # pass 'u' and row indices 'i' to the pool
    from itertools import repeat
    tmp = pool.starmap(A_sum, zip(repeat(u), r))
    return pool.starmap(At_sum, zip(repeat(tmp), r))

def main():
    global memo_matrix
    n = int(argv[1])
    
    # G18: build the lookup table before any heavy processing starts
    memo_matrix = [[eval_A(i, j) for j in range(n)] for i in range(n)]

    u = [1.0] * n

    # Pool must be created after memo_matrix is populated
    # on Windows, use an initializer so worker processes receive the memo table
    with Pool(processes=4, initializer=init_worker, initargs=(memo_matrix,)) as pool:
        for _ in range(10):
            v = multiply_AtAv(u, pool, n)
            u = multiply_AtAv(v, pool, n)

        vBv = vv = 0.0
        for ue, ve in zip(u, v):
            vBv += ue * ve
            vv  += ve * ve

        result = sqrt(vBv / vv)
        print("{0:.9f}".format(result))

if __name__ == '__main__':
    main()
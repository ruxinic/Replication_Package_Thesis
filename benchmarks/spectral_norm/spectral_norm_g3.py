from itertools import repeat
from math import sqrt
from multiprocessing import Pool
from sys import argv

def eval_A(i, j):
    ij = i + j
    return 1.0 / (ij * (ij + 1) / 2 + i + 1)

def A_sum(u, i):
    x = 0
    local_eval = eval_A  # G3: local variable caching
    # G3: ensure the loop end is constant
    u_len = len(u) 
    for j in range(u_len):
        x += local_eval(i, j) * u[j]
    return x

def At_sum(u, i):
    x = 0
    local_eval = eval_A
    u_len = len(u)
    for j in range(u_len):
        x += local_eval(j, i) * u[j]
    return x

def multiply_AtAv(u, pool):
    l = len(u)
    r = range(l)
    
    tmp = pool.starmap(A_sum, zip(repeat(u), r))
    return pool.starmap(At_sum, zip(repeat(tmp), r))

def main():
    n = int(argv[1])
    u = [1.0] * n
    
    # G3: store the pool reference locally
    with Pool(processes=4) as pool:
        for _ in range(10):
            v = multiply_AtAv(u, pool)
            u = multiply_AtAv(v, pool)

        vBv = 0.0
        vv = 0.0
        # G3: use a single loop for final reduction (Loop Fusion)
        for i in range(n):
            ui = u[i]
            vi = v[i]
            vBv += ui * vi
            vv  += vi * vi

        print("{0:.9f}".format(sqrt(vBv / vv)))

if __name__ == '__main__':
    main()
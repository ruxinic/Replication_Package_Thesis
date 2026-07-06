from itertools import repeat
from math import sqrt
from multiprocessing import Pool
from sys import argv

# Baseline had: x += eval_A(i, j) * u_j 
# G17: avoid the function call entirely inside the loop

def A_sum(u, i):
    x = 0
    # G17: put the length call outside the loop
    u_len = len(u) 
    
    # G17: inline the logic of eval_A 
    for j in range(u_len):
        # perform the math directly instead of calling eval_A(i, j)
        ij = i + j
        # static formula calculated in-place
        eval_val = 1.0 / (ij * (ij + 1) / 2 + i + 1)
        x += eval_val * u[j]
    return x

def At_sum(u, i):
    x = 0
    u_len = len(u)
    for j in range(u_len):
        # G17: inline the math to avoid function call overhead
        ji = j + i
        eval_val = 1.0 / (ji * (ji + 1) / 2 + j + 1)
        x += eval_val * u[j]
    return x


def multiply_AtAv(u):
    r = range(len(u))

    tmp = pool.starmap(
        A_sum,
        zip(repeat(u), r)
    )
    return pool.starmap(
        At_sum,
        zip(repeat(tmp), r)
    )


def main():
    n = int(argv[1])
    u = [1] * n

    for _ in range(10):
        v = multiply_AtAv(u)
        u = multiply_AtAv(v)

    vBv = vv = 0

    for ue, ve in zip(u, v):
        vBv += ue * ve
        vv  += ve * ve

    result = sqrt(vBv/vv)
    print("{0:.9f}".format(result))


if __name__ == '__main__':
    with Pool(processes=4) as pool:
        main()

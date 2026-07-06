from itertools import repeat
from math import sqrt
from multiprocessing import Pool
from sys import argv


def eval_A(i, j):
    ij = i + j
    ij_1 = ij + 1 # G1: assign expression to variable for later reuse
    res = ij * ij_1 / 2 + i + 1
    return 1.0 / res


def A_sum(u, i):
    x = 0
    for j, u_j in enumerate(u):
        y = eval_A(i, j) * u_j # G1: assign expression to variable
        x += y
    return x


def At_sum(u, i):
    x = 0
    for j, u_j in enumerate(u):
        y = eval_A(j, i) * u_j # G1: assign expression to variable
        x += y
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
        ueve = ue * ve # G1: assign expression to variable
        veve = ve * ve 
        vBv += ueve
        vv  += veve

    result = sqrt(vBv/vv)
    print("{0:.9f}".format(result))


if __name__ == '__main__':
    with Pool(processes=4) as pool:
        main()

from math import sqrt
from multiprocessing import Pool
from sys import argv

# G19: remove the 'def eval_A' entirely
def A_sum(u, i):
    x = 0.0
    # G19: localize the variable 'u' and 'range' to avoid global/scope lookups
    local_u = u
    u_len = len(local_u)
    
    for j in range(u_len):
        # G19: inline code; the math from eval_A is placed directly here
        ij = i + j
        x += (1.0 / (ij * (ij + 1) / 2 + i + 1)) * local_u[j]
    return x

def At_sum(u, i):
    x = 0.0
    local_u = u
    u_len = len(local_u)
    
    for j in range(u_len):
        # G19: inline code for the transpose logic
        ji = j + i
        x += (1.0 / (ji * (ji + 1) / 2 + j + 1)) * local_u[j]
    return x

def main():
    n = int(argv[1])
    u = [1.0] * n
    
    # G19: save the sqrt function
    local_sqrt = sqrt

    with Pool(processes=4) as pool:
        from itertools import repeat
        for _ in range(10):
            # multiply_AtAv logic inlined here
            tmp = pool.starmap(A_sum, zip(repeat(u), range(n)))
            v = pool.starmap(At_sum, zip(repeat(tmp), range(n)))
            
            tmp = pool.starmap(A_sum, zip(repeat(v), range(n)))
            u = pool.starmap(At_sum, zip(repeat(tmp), range(n)))

        vBv = vv = 0.0
        for i in range(n):
            ui = u[i]
            vi = v[i]
            vBv += ui * vi
            vv  += vi * vi

        # G19: use the localized function reference
        print("{0:.9f}".format(local_sqrt(vBv / vv)))

if __name__ == '__main__':
    main()
from math import sqrt
from sys import argv

def main():
    n = int(argv[1]) if len(argv) > 1 else 100
    u = [1.0] * n
    
    # G6: only create one matrix (memo_A)
    memo_A = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            ij = i + j
            memo_A[i][j] = 1.0 / (ij * (ij + 1) / 2 + i + 1)

    for _ in range(10):
        # multiply by A: Accessing rows directly (memo_A[i])
        tmp = [sum(memo_A[i][j] * u[j] for j in range(n)) for i in range(n)]
        
        # multiply by At: Instead of a second matrix, we swap indices [j][i].
        v = [sum(memo_A[j][i] * tmp[j] for j in range(n)) for i in range(n)]
        
        # repeat the process to update u
        tmp = [sum(memo_A[i][j] * v[j] for j in range(n)) for i in range(n)]
        u = [sum(memo_A[j][i] * tmp[j] for j in range(n)) for i in range(n)]

    vBv = sum(ue * ve for ue, ve in zip(u, v))
    vv = sum(ve * ve for ve in v)
    
    print("{0:.9f}".format(sqrt(vBv/vv)))

if __name__ == '__main__':
    main()
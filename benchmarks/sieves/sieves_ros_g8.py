import ctypes
import os
import sys

lib_path = os.path.abspath("./sieves_lib.so")
_lib = ctypes.CDLL(lib_path)

_lib.compute_sieve.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int)
]
_lib.compute_sieve.restype = ctypes.c_int


def primes_upto(limit):
    # Prime Number Theorem approximation to size the output buffer 
    # (pi(x) approx x/ln(x)). For 100M, there are exactly 5,761,455 primes
    estimated_max_primes = int(limit / 2) if limit > 10 else limit
    PrimeBuffer = ctypes.c_int * estimated_max_primes
    out_primes = PrimeBuffer()

    # heavy nested loops are executed entirely in C
    total_primes = _lib.compute_sieve(limit, out_primes)

    # convert the raw memory array back to a standard Python list slice
    return list(out_primes[:total_primes])


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100000000
    
    primes = primes_upto(limit)
    print(f"Found {len(primes)} primes up to {limit}.")
    if len(primes) > 0:
        print(f"Last prime found: {primes[-1]}")


if __name__ == '__main__':
    main()
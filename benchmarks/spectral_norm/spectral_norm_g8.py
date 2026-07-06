import ctypes
import math
import os
import sys

lib_path = os.path.abspath("./spectral.so")
try:
    _lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"Error loading shared library: {e}")
    sys.exit(1)

_lib.multiply_AtAv.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double)
]
_lib.multiply_AtAv.restype = None


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100

    # sllocate contiguous hardware-level arrays directly via ctypes
    DoubleArray = ctypes.c_double * n
    u = DoubleArray(*([1.0] * n))
    v = DoubleArray(*([0.0] * n))
    tmp = DoubleArray(*([0.0] * n))

    # run the heavy mathematical optimization passes
    for _ in range(10):
        # computes v = AtAv(u)
        _lib.multiply_AtAv(n, u, v, tmp)
        # computes u = AtAv(v)
        _lib.multiply_AtAv(n, v, u, tmp)

    vBv = 0.0
    vv = 0.0

    # calculate final dot products
    for ue, ve in zip(u, v):
        vBv += ue * ve
        vv += ve * ve

    result = math.sqrt(vBv / vv)
    print(f"{result:.9f}")


if __name__ == '__main__':
    main()
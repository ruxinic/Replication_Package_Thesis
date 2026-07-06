import ctypes
import os
import sys
import numpy as np

lib_path = os.path.abspath("./mnd_lib1.so")
_lib = ctypes.CDLL(lib_path)

_lib.compute_mandelbrot.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
    np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
    np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C_CONTIGUOUS')
]
_lib.compute_mandelbrot.restype = None


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    X = np.linspace(-2.0, 0.5, N, dtype=np.float64)
    Y = np.linspace(-1.0, 1.0, N, dtype=np.float64)
    Z = np.zeros((len(Y), len(X)), dtype=np.float64)

    # explicitly extract array matrix metadata shapes
    # Z.shape[0] is height (rows), Z.shape[1] is width (columns)
    height, width = Z.shape

    _lib.compute_mandelbrot(width, height, X, Y, Z)

    print(f"Checksum: {int(Z.sum())}")

if __name__ == "__main__":
    main()
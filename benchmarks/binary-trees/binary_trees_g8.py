import sys
import ctypes
import multiprocessing as mp
from os import path

_lib = None

def worker_init():
    # initialize the external C library for an isolated worker execution thread
    global _lib
    lib_name = "./tree_lib.so"
    lib_path = path.abspath(lib_name)
    
    _lib = ctypes.CDLL(lib_path)
    _lib.make_check.restype = ctypes.c_int
    _lib.make_check.argtypes = [ctypes.c_int]
    
    # Bindings for manual tree lifespan management
    _lib.make_tree.restype = ctypes.c_void_p
    _lib.make_tree.argtypes = [ctypes.c_int]
    
    _lib.check_tree.restype = ctypes.c_int
    _lib.check_tree.argtypes = [ctypes.c_void_p]
    
    _lib.free_tree.restype = None
    _lib.free_tree.argtypes = [ctypes.c_void_p]

def call_make_check(dd):
    return _lib.make_check(dd)

def main(n, min_depth=4):
    max_depth = max(min_depth + 2, n)
    stretch_depth = max_depth + 1

    worker_init()

    # stretch Tree evaluation (Transient allocation block)
    print(f'stretch tree of depth {stretch_depth}\t check: {call_make_check(stretch_depth)}')

    # allocate long_lived_tree directly onto native memory heap
    # store the reference pointer address instead of discarding it immediately
    long_lived_tree = _lib.make_tree(max_depth)

    if mp.cpu_count() > 1:
        pool = mp.Pool(initializer=worker_init)
        chunkmap = pool.map
    else:
        chunkmap = map

    mmd = max_depth + min_depth
    for dd in range(min_depth, stretch_depth, 2):
        ii = 2 ** (mmd - dd)
        cs = sum(chunkmap(call_make_check, [dd] * ii))
        print(f'{ii}\t trees of depth {dd}\t check: {cs}')

    # check the long lived tree while it is still alive in memory
    ll_check = _lib.check_tree(long_lived_tree)
    print(f'long lived tree of depth {max_depth}\t check: {ll_check}')
    
    # clean up the memory right before exiting to prevent memory leaks
    _lib.free_tree(long_lived_tree)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
import sys
import multiprocessing as mp

# G19: using a helper to inline the tree creation and checking logic
# it reduces the number of function calls to 'make_check'
def make_check_inline(dd):    
    # recursive make_tree logic
    def _make(d):
        if d > 0:
            return (_make(d-1), _make(d-1))
        return (None, None)
    
    # recursive check_tree logic
    def _check(node):
        l, r = node
        if l is None:
            return 1
        return 1 + _check(l) + _check(r)
    
    # G19: executing the operations within a single scope 
    return _check(_make(dd))

def main(n, min_depth=4):
    max_depth = max(min_depth + 2, n)
    stretch_depth = max_depth + 1

    if mp.cpu_count() > 1:
        pool = mp.Pool()
        chunkmap = pool.map
    else:
        chunkmap = map

    # G19: direct execution to avoid unnecessary overhead for single calls
    print('stretch tree of depth {0}\t check: {1}'.format(
          stretch_depth, make_check_inline(stretch_depth)))

    # G19: for the long-lived tree, use inline logic for the check
    long_lived_tree = (lambda d: (lambda f, n: f(f, n))(lambda f, i: (f(f, i-1), f(f, i-1)) if i > 0 else (None, None), d))(max_depth)

    mmd = max_depth + min_depth
    for dd in range(min_depth, stretch_depth, 2):
        ii = 2 ** (mmd - dd)
        # G19: chunkmap calls 'make_check_inline' which handles its own logic, 
        # reducing the total number of cross-function jumps
        cs = sum(chunkmap(make_check_inline, (dd,)*ii))
        print('{0}\t trees of depth {1}\t check: {2}'.format(ii, dd, cs))

    # G19: reducing lookup delays by using local references
    check = lambda node: (1 + check(node[0]) + check(node[1])) if node[0] is not None else 1
    print('long lived tree of depth {0}\t check: {1}'.format(
          max_depth, check(long_lived_tree)))

if __name__ == '__main__':
    main(int(sys.argv[1]))
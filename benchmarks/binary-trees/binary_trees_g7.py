# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# contributed by Antoine Pitrou
# modified by Dominique Wahli and Daniel Nanz
# modified by Joerg Baumann
# modified by Jonathan Ultis

import sys
import multiprocessing as mp

def make_tree(dd):
    if dd > 0:
        return (make_tree(dd-1), make_tree(dd-1))
    return (None, None)

def check_tree(node):
    l, r = node
    if l is None:
        return 1
    else:
        return 1 + check_tree(l) + check_tree(r)

# G7: bulk operation function runs a loop inside the worker to reduce communication overhead
def bulk_make_check(args):
    depth, iterations = args
    total_check = 0
    for _ in range(iterations):
        # the 'function call' overhead happens only once for 'iterations' trees
        total_check += check_tree(make_tree(depth))
    return total_check

def main(n, min_depth=4):
    max_depth = max(min_depth + 2, n)
    stretch_depth = max_depth + 1
    print(f'stretch tree of depth {stretch_depth}\t check: {check_tree(make_tree(stretch_depth))}')

    long_lived_tree = make_tree(max_depth)

    mmd = max_depth + min_depth
    
    if mp.cpu_count() > 1:
        pool = mp.Pool()
        # G7: use a smaller number of larger tasks
        num_workers = mp.cpu_count()
    else:
        pool = None

    for dd in range(min_depth, stretch_depth, 2):
        total_trees = 2 ** (mmd - dd)
        
        if pool:
            # G7: divide total_trees into 'num_workers' chunks; instead of total_trees tasks, only send 'num_workers' tasks
            trees_per_worker = total_trees // num_workers
            remaining = total_trees % num_workers
            
            tasks = [(dd, trees_per_worker)] * num_workers
            if remaining > 0:
                tasks.append((dd, remaining))
            
            # bulk operation
            results = pool.map(bulk_make_check, tasks)
            cs = sum(results)
        else:
            cs = bulk_make_check((dd, total_trees))
            
        print(f'{total_trees}\t trees of depth {dd}\t check: {cs}')

    print(f'long lived tree of depth {max_depth}\t check: {check_tree(long_lived_tree)}')

if __name__ == '__main__':
    main(int(sys.argv[1]))
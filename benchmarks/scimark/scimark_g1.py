from array import array
import math

import pyperf as perf

class Array2D(object):

    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        size = w * h
        self.data = array('d', [0]) * (size)
        if data is not None:
            self.setup(data)

    def _idx(self, x, y):
        w = self.width
        h = self.height
        # g1
        if 0 <= x < w and 0 <= y < h:
            return y * w + x
        raise IndexError
    
    def __getitem__(self, x_y):
        (x, y) = x_y
        return self.data[self._idx(x, y)]

    def __setitem__(self, x_y, val):
        (x, y) = x_y
        self.data[self._idx(x, y)] = val

    def setup(self, data):
        h = self.height
        w = self.width
        for y in range(h):
            row = data[y] # g1
            for x in range(w):
                self[x, y] = row[x]
        return self
    
    def indexes(self):
        h = self.height
        w = self.width
        for y in range(h):
            for x in range(w):
                yield x, y

    def copy_data_from(self, other):
        self.data[:] = other.data[:]


class Random(object):
    MDIG = 32
    ONE = 1
    # g1
    _shift_val = (ONE << (MDIG - 2))
    m1 = _shift_val + (_shift_val - ONE)
    m2 = ONE << MDIG // 2
    dm1 = 1.0 / float(m1)

    def __init__(self, seed):
        self.initialize(seed)
        self.left = 0.0
        self.right = 1.0
        self.width = 1.0
        self.haveRange = False

    def initialize(self, seed):
        self.seed = seed
        jseed = min(abs(seed), self.m1)
        if (jseed % 2 == 0):
            jseed -= 1
        
        m2 = self.m2 # g1
        k0 = 9069 % m2
        k1 = 9069 / m2
        j0 = jseed % m2
        j1 = jseed / m2
        self.m = array('d', [0]) * 17
        
        m2_half = m2 / 2 # G1: pre-calculate repeated division
        for iloop in range(17):
            jseed_prod = j0 * k0 # G1: local variable for product
            j1 = (jseed_prod / m2 + j0 * k1 + j1 * k0) % m2_half
            j0 = jseed_prod % m2
            self.m[iloop] = j0 + m2 * j1
        self.i = 4
        self.j = 16

    def nextDouble(self):
        I, J, m = self.i, self.j, self.m
        k = m[I] - m[J]
        if (k < 0):
            k += self.m1
        self.m[J] = k

        # G1: optimized repetitive assignment logic
        new_I = 16 if I == 0 else I - 1
        self.i = new_I

        new_J = 16 if J == 0 else J - 1
        self.j = new_J

        val_k = self.dm1 * float(k) # G1: shared expression in both branches
        if (self.haveRange):
            return self.left + val_k * self.width
        else:
            return val_k
        
    def RandomMatrix(self, a):
        nxt = self.nextDouble # g1
        for x, y in a.indexes():
            a[x, y] = nxt()
        return a

    def RandomVector(self, n):
        nxt = self.nextDouble
        return array('d', [nxt() for i in range(n)])

def copy_vector(vec):
    # Copy a vector created by Random.RandomVector()
    vec2 = array('d')
    vec2[:] = vec[:]
    return vec2


class ArrayList(Array2D):

    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        self.data = [array('d', [0]) * w for y in range(h)]
        if data is not None:
            self.setup(data)

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self.data[idx[1]][idx[0]]
        else:
            return self.data[idx]

    def __setitem__(self, idx, val):
        if isinstance(idx, tuple):
            self.data[idx[1]][idx[0]] = val
        else:
            self.data[idx] = val

    def copy_data_from(self, other):
        for l1, l2 in zip(self.data, other.data):
            l1[:] = l2


def SOR_execute(omega, G, cycles, Array):
    # G1: cache attributes and expressions
    h = G.height - 1
    w = G.width - 1
    om_factor = omega * 0.25
    inv_om = 1.0 - omega
    
    for p in range(cycles):
        for y in range(1, h):
            y_up = y - 1
            y_down = y + 1
            for x in range(1, w):
                # G1: pre-calculate neighbor indices
                # cache neighbour sums
                G[x, y] = (om_factor * (G[x, y_up] + G[x, y_down] + G[x - 1, y] + G[x + 1, y])
                           + inv_om * G[x, y])

def bench_SOR(loops, n, cycles, Array):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        G = Array(n, n)
        SOR_execute(1.25, G, cycles, Array)

    return perf.perf_counter() - t0


def SparseCompRow_matmult(M, y, val, row, col, x, num_iterations):
    range_it = range(num_iterations)
    t0 = perf.perf_counter()

    for _ in range_it:
        for r in range(M):
            sa = 0.0
            # G1: cache row bounds to avoid repeated indexing
            r_start = row[r]
            r_end = row[r + 1]
            for i in range(r_start, r_end):
                sa += x[col[i]] * val[i]
            y[r] = sa

    return perf.perf_counter() - t0

def bench_SparseMatMult(cycles, N, nz):
    x = array('d', [0]) * N
    y = array('d', [0]) * N

    nr = nz // N
    anz = nr * N
    val = array('d', [0]) * anz
    col = array('i', [0]) * nz
    row = array('i', [0]) * (N + 1)

    row[0] = 0
    for r in range(N):
        rowr = row[r]
        step = r // nr
        row[r + 1] = rowr + nr
        if step < 1:
            step = 1
        for i in range(nr):
            col[rowr + i] = i * step

    return SparseCompRow_matmult(N, y, val, row, col, x, cycles)


def MonteCarlo(Num_samples):
    rnd = Random(113)
    nxt = rnd.nextDouble # G1: cache method lookup
    under_curve = 0
    for count in range(Num_samples):
        x = nxt()
        y = nxt()
        if (x * x + y * y) <= 1.0: # G1: expression occurs once, but nxt() was duplicated
            under_curve += 1
    # G1: cache Num_samples as float to avoid multiple conversions
    return float(under_curve) / Num_samples * 4.0

def bench_MonteCarlo(loops, Num_samples):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        MonteCarlo(Num_samples)

    return perf.perf_counter() - t0


def LU_factor(A, pivot):
    M, N = A.height, A.width
    minMN = min(M, N)
    for j in range(minMN):
        jp = j
        # G1: cache repeated row/column access
        row_j = A[j]
        t = abs(row_j[j])
        for i in range(j + 1, M):
            row_i = A[i]
            ab = abs(row_i[j])
            if ab > t:
                jp = i
                t = ab
        pivot[j] = jp

        if A[jp][j] == 0:
            raise Exception("factorization failed because of zero pivot")

        if jp != j:
            A[j], A[jp] = A[jp], A[j]

        # refresh row reference after swap
        row_j = A[j]
        if j < M - 1:
            recp = 1.0 / row_j[j]
            for k in range(j + 1, M):
                A[k][j] *= recp

        if j < minMN - 1:
            for ii in range(j + 1, M):
                row_ii = A[ii]
                multiplier = row_ii[j] # G1: cache A[ii][j]
                for jj in range(j + 1, N):
                    row_ii[jj] -= multiplier * row_j[jj]

def LU(lu, A, pivot):
    lu.copy_data_from(A)
    LU_factor(lu, pivot)


def bench_LU(cycles, N):
    rnd = Random(7)
    A = rnd.RandomMatrix(ArrayList(N, N))
    lu = ArrayList(N, N)
    pivot = array('i', [0]) * N
    range_it = range(cycles)
    t0 = perf.perf_counter()

    for _ in range_it:
        LU(lu, A, pivot)

    return perf.perf_counter() - t0


def int_log2(n):
    k = 1
    log = 0
    while k < n:
        k *= 2
        log += 1
    if n != 1 << log:
        raise Exception("FFT: Data length is not a power of 2: %s" % n)
    return log


def FFT_num_flops(N):
    return (5.0 * N - 2) * int_log2(N) + 2 * (N + 1)


def FFT_transform_internal(N, data, direction):
    n = N // 2
    if n == 1 or N == 0:
        return

    logn = int_log2(n)
    FFT_bitreverse(N, data)

    dual = 1
    for bit in range(logn):
        w_real, w_imag = 1.0, 0.0
        # G1: cache repeated math operations
        angle = 2.0 * direction * math.pi / (2.0 * float(dual))
        s = math.sin(angle)
        t = math.sin(angle / 2.0)
        s2 = 2.0 * t * t
        
        two_dual = 2 * dual # G1: pre-calculate loop step
        for b in range(0, n, two_dual):
            i = 2 * b
            j = i + two_dual # G1: simplify index calculation
            i_p1 = i + 1
            j_p1 = j + 1
            
            wd_real = data[j]
            wd_imag = data[j_p1]
            data[j] = data[i] - wd_real
            data[j_p1] = data[i_p1] - wd_imag
            data[i] += wd_real
            data[i_p1] += wd_imag
            
        for a in range(1, dual):
            # G1: cache products used in tmp calculation
            s_w_imag = s * w_imag
            s2_w_real = s2 * w_real
            s_w_real = s * w_real
            s2_w_imag = s2 * w_imag
            
            tmp_real = w_real - s_w_imag - s2_w_real
            tmp_imag = w_imag + s_w_real - s2_w_imag
            w_real, w_imag = tmp_real, tmp_imag
            
            for b in range(0, n, two_dual):
                common_idx = 2 * (b + a) # G1: cache shared base index
                i = common_idx
                j = common_idx + two_dual
                i_p1, j_p1 = i + 1, j + 1
                
                z1_real, z1_imag = data[j], data[j_p1]
                wd_real = w_real * z1_real - w_imag * z1_imag
                wd_imag = w_real * z1_imag + w_imag * z1_real
                
                data[j] = data[i] - wd_real
                data[j_p1] = data[i_p1] - wd_imag
                data[i] += wd_real
                data[i_p1] += wd_imag
        dual *= 2

def FFT_bitreverse(N, data):
    n = N // 2
    nm1 = n - 1
    j = 0
    for i in range(nm1):
        ii = i << 1
        jj = j << 1
        k = n >> 1
        if i < j:
            # G1: cache the incremented indices
            ii_p1 = ii + 1
            jj_p1 = jj + 1
            tmp_real = data[ii]
            tmp_imag = data[ii_p1]
            data[ii] = data[jj]
            data[ii_p1] = data[jj_p1]
            data[jj] = tmp_real
            data[jj_p1] = tmp_imag
        while k <= j:
            j -= k
            k >>= 1
        j += k

def FFT_transform(N, data):
    FFT_transform_internal(N, data, -1)


def FFT_inverse(N, data):
    n = N / 2
    norm = 0.0
    fl = float(n) #G1: assign to variable
    FFT_transform_internal(N, data, +1)
    norm = 1 / fl
    for i in range(N):
        data[i] *= norm


def bench_FFT(loops, N, cycles):
    twoN = 2 * N
    init_vec = Random(7).RandomVector(twoN)
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        x = copy_vector(init_vec)
        for i in range(cycles):
            FFT_transform(twoN, x)
            FFT_inverse(twoN, x)

    return perf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    if args.benchmark:
        cmd.append(args.benchmark)


BENCHMARKS = {
    # function name => arguments
    'sor': (bench_SOR, 100, 10, Array2D),
    'sparse_mat_mult': (bench_SparseMatMult, 50000, 1000000),
    'monte_carlo': (bench_MonteCarlo, 1000000),
    'lu': (bench_LU, 256),
    'fft': (bench_FFT, 16384, 7),
}


if __name__ == "__main__":
    runner = perf.Runner(add_cmdline_args=add_cmdline_args)
    runner.argparser.add_argument("benchmark", nargs='?',
                                  choices=sorted(BENCHMARKS))

    args = runner.parse_args()
    if args.benchmark:
        benchmarks = (args.benchmark,)
    else:
        benchmarks = sorted(BENCHMARKS)

    for bench in benchmarks:
        name = 'scimark_%s' % bench
        args = BENCHMARKS[bench]
        runner.bench_time_func(name, *args)
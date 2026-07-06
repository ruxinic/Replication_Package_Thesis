from array import array
import math

import pyperf as perf

class Array2D(object):

    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        self.data = array('d', [0]) * (w * h)
        if data is not None:
            self.setup(data)

    #def _idx(self, x, y):
     #   if 0 <= x < self.width and 0 <= y < self.height:
      #      return y * self.width + x
       # raise IndexError
    #G19: it will not call these functions; we're inlining them
    def __getitem__(self, x_y):
    # G19: direct indexing to avoid function call overhead
        # x_y is the tuple (x, y)
        return self.data[x_y[1] * self.width + x_y[0]]

    def __setitem__(self, x_y, val):
        # G19: direct calculation of flat array index
        self.data[x_y[1] * self.width + x_y[0]] = val

    def setup(self, data):
        w, h, d_array = self.width, self.height, self.data
        for y in range(h):
            row = data[y]
            offset = y * w
            for x in range(w):
                d_array[offset + x] = row[x]
        return self

    def indexes(self):
        w, h = self.width, self.height
        for y in range(h):
            for x in range(w):
                yield x, y

    def copy_data_from(self, other):
        self.data[:] = other.data[:]


class Random(object):
    MDIG = 32
    ONE = 1
    m1 = (ONE << (MDIG - 2)) + ((ONE << (MDIG - 2)) - ONE)
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
        seed = abs(seed)
        m1, m2 = self.m1, self.m2
        jseed = min(seed, self.m1)
        if (jseed % 2 == 0):
            jseed -= 1
        k0 = 9069 % self.m2
        k1 = 9069 / self.m2
        j0 = jseed % self.m2
        j1 = jseed / self.m2
        self.m = array('d', [0]) * 17
        m_arr = self.m
        for iloop in range(17):
            jseed = j0 * k0
            j1 = (jseed / m2 + j0 * k1 + j1 * k0) % (m2 / 2)
            j0 = jseed % m2
            m_arr[iloop] = j0 + m2 * j1
        self.i = 4
        self.j = 16

    def nextDouble(self):
        I, J, m = self.i, self.j, self.m
        m1, dm1 = self.m1, self.dm1
        
        k = m[I] - m[J]
        if (k < 0):
            k += m1
        m[J] = k

        I = 16 if I == 0 else I - 1
        J = 16 if J == 0 else J - 1
        
        self.i, self.j = I, J

        if (self.haveRange):
            return self.left + dm1 * float(k) * self.width
        return dm1 * float(k)
    
    def RandomMatrix(self, a):
# G19: localize parameters
        nxt = self.nextDouble
        d_data = a.data
        
        # check if we are dealing with ArrayList (list of rows) 
        # or Array2D (one flat array)
        if isinstance(d_data, list):
            # ArrayList path: iterate through rows
            for row in d_data:
                for i in range(len(row)):
                    row[i] = nxt()
        else:
            # Array2D path: iterate through flat array
            for i in range(len(d_data)):
                d_data[i] = nxt()
        return a
        
    def RandomVector(self, n):
        nxt = self.nextDouble
        return array('d', [nxt() for _ in range(n)])

def copy_vector(vec):
    # Copy a vector created by Random.RandomVector()
    vec2 = array('d')
    vec2[:] = vec[:]
    return vec2


class ArrayList(Array2D):

    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        self.data = [array('d', [0.0]) * w for _ in range(h)]
        if data is not None:
            self.setup(data)

    def setup(self, data):
        # G19: override parent setup to handle nested list structure efficiently
        # localize data for faster access
        target_data = self.data
        for y in range(self.height):
            # Copy row-by-row for speed
            target_data[y][:] = array('d', data[y])
        return self
    
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


def SOR_execute(omega, G, cycles):
# G19: inline __getitem__/__setitem__ by accessing G.data directly
    w, h, data = G.width, G.height, G.data
    om_025 = omega * 0.25
    one_minus_om = 1.0 - omega
    
    for _ in range(cycles):
        for y in range(1, h - 1):
            offset = y * w
            off_up = (y - 1) * w
            off_down = (y + 1) * w
            for x in range(1, w - 1):
                # manual index calculation to avoid method calls
                curr_idx = offset + x
                data[curr_idx] = (om_025 * (data[off_up + x] + data[off_down + x] + 
                                            data[curr_idx - 1] + data[curr_idx + 1]) +
                                  (one_minus_om * data[curr_idx]))

def bench_SOR(loops, n, cycles, Array):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        G = Array(n, n)
        SOR_execute(1.25, G, cycles)

    return perf.perf_counter() - t0


def SparseCompRow_matmult(M, y, val, row, col, x, num_iterations):
# G19: localize everything before the loops
    _range = range
    t0 = perf.perf_counter()

    for _ in _range(num_iterations):
        for r in _range(M):
            sa = 0.0
            # G19: localize the start and end indices to avoid repeated row[r] lookups
            row_start = row[r]
            row_end = row[r + 1]
            for i in _range(row_start, row_end):
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
    # G19: localize the method to avoid attribute lookup in the loop
    nxt = rnd.nextDouble
    under_curve = 0
    for _ in range(Num_samples):
        x = nxt()
        y = nxt()
        if x * x + y * y <= 1.0:
            under_curve += 1
    return float(under_curve) / Num_samples * 4.0

def bench_MonteCarlo(loops, Num_samples):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        MonteCarlo(Num_samples)

    return perf.perf_counter() - t0


def LU_factor(A, pivot):
    M, N, data = A.height, A.width, A.data
    minMN = min(M, N)
    for j in range(minMN):
        jp = j
        t = abs(data[j][j]) # direct row access for ArrayList
        for i in range(j + 1, M):
            ab = abs(data[i][j])
            if ab > t:
                jp = i
                t = ab
        pivot[j] = jp

        if data[jp][j] == 0:
            raise Exception("factorization failed: zero pivot")

        if jp != j:
            data[j], data[jp] = data[jp], data[j]

        if j < M - 1:
            recp = 1.0 / data[j][j]
            row_j = data[j]
            for k in range(j + 1, M):
                data[k][j] *= recp

        if j < minMN - 1:
            # G19: cache row_j to avoid repeated lookups in the inner loop
            for ii in range(j + 1, M):
                row_ii = data[ii]
                multiplier = row_ii[j]
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
    bit = 0
    dual = 1
    if n == 1:
        return

    logn = int_log2(n)
    if N == 0:
        return
    FFT_bitreverse(N, data)

    # apply fft recursion
    # this loop executed int_log2(N) times
    _sin = math.sin # G19: Localize global function
    _pi = math.pi
    _range = range
    
    while bit < logn:
        w_real = 1.0
        w_imag = 0.0
        theta = 2.0 * direction * _pi / (2.0 * float(dual))
        s = _sin(theta)
        t = _sin(theta / 2.0)
        s2 = 2.0 * t * t       
        # G19: localize dual to avoid repeated while-scope lookups
        local_dual = dual
        double_dual = local_dual << 1
        two_n = n << 1 # Equivalent to 2*n 
        for b in _range(0, n, double_dual):
            i = b << 1
            j = (b + local_dual) << 1
# inline math for the first element (where w_real=1, w_imag=0)
            data_i = data[i]
            data_i_1 = data[i + 1]
            data_j = data[j]
            data_j_1 = data[j + 1]
            
            data[j] = data_i - data_j
            data[j + 1] = data_i_1 - data_j_1
            data[i] = data_i + data_j
            data[i + 1] = data_i_1 + data_j_1
            
        for a in _range(1, local_dual):
            # update complex multiplier (w_real, w_imag)
            tmp_real = w_real - s * w_imag - s2 * w_real
            tmp_imag = w_imag + s * w_real - s2 * w_imag
            w_real = tmp_real
            w_imag = tmp_imag
            
            for b in _range(0, n, double_dual):
                i = (b + a) << 1
                j = (b + a + local_dual) << 1
                
                z1_real = data[j]
                z1_imag = data[j + 1]
                
                # butterfly calculation
                wd_real = w_real * z1_real - w_imag * z1_imag
                wd_imag = w_real * z1_imag + w_imag * z1_real
                
                data_i_real = data[i]
                data_i_imag = data[i + 1]
                
                data[j] = data_i_real - wd_real
                data[j + 1] = data_i_imag - wd_imag
                data[i] = data_i_real + wd_real
                data[i + 1] = data_i_imag + wd_imag
        
        bit += 1
        dual = double_dual

def FFT_bitreverse(N, data):
    n = N // 2
    nm1 = n - 1
    j = 0
    for i in range(nm1):
        ii = i << 1
        jj = j << 1
        k = n >> 1
        if i < j:
            tmp_real = data[ii]
            tmp_imag = data[ii + 1]
            data[ii] = data[jj]
            data[ii + 1] = data[jj + 1]
            data[jj] = tmp_real
            data[jj + 1] = tmp_imag
        while k <= j:
            j -= k
            k >>= 1
        j += k


def FFT_transform(N, data):
    FFT_transform_internal(N, data, -1)


def FFT_inverse(N, data):
    n = N / 2
    norm = 0.0
    FFT_transform_internal(N, data, +1)
    norm = 1 / float(n)
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
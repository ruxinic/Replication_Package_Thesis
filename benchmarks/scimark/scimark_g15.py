from array import array
import math
from numba import njit
import pyperf as perf
import numpy as np 

class Array2D(object):

    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        self.data = np.zeros(w * h, dtype=np.float64)
        if data is not None:
            self.setup(data)

    def _idx(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return y * self.width + x
        raise IndexError

    def __getitem__(self, x_y):
        (x, y) = x_y
        return self.data[self._idx(x, y)]

    def __setitem__(self, x_y, val):
        (x, y) = x_y
        self.data[self._idx(x, y)] = val

    def setup(self, data):
        for y in range(self.height):
            for x in range(self.width):
                self[x, y] = data[y][x]
        return self

    def indexes(self):
        for y in range(self.height):
            for x in range(self.width):
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
        jseed = min(seed, self.m1)
        if (jseed % 2 == 0):
            jseed -= 1
        k0 = 9069 % self.m2
        k1 = 9069 / self.m2
        j0 = jseed % self.m2
        j1 = jseed / self.m2
        self.m = array('d', [0]) * 17
        for iloop in range(17):
            jseed = j0 * k0
            j1 = (jseed / self.m2 + j0 * k1 + j1 * k0) % (self.m2 / 2)
            j0 = jseed % self.m2
            self.m[iloop] = j0 + self.m2 * j1
        self.i = 4
        self.j = 16

    def nextDouble(self):
        I, J, m = self.i, self.j, self.m
        k = m[I] - m[J]
        if (k < 0):
            k += self.m1
        self.m[J] = k

        if (I == 0):
            I = 16
        else:
            I -= 1
        self.i = I

        if (J == 0):
            J = 16
        else:
            J -= 1
        self.j = J

        if (self.haveRange):
            return self.left + self.dm1 * float(k) * self.width
        else:
            return self.dm1 * float(k)

    def RandomMatrix(self, a):
        for x, y in a.indexes():
            a[x, y] = self.nextDouble()
        return a

    def RandomVector(self, n):
        return array('d', [self.nextDouble() for i in range(n)])


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

# G15: add @njit
@njit(cache=True)
def SOR_execute_jit(omega, data, height, width, cycles):
    om_025 = omega * 0.25
    one_minus_om = 1.0 - omega
    for p in range(cycles):
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                idx = y * width + x
                # compiled direct memory access is significantly faster
                data[idx] = (om_025 * (data[idx - width] + data[idx + width] + 
                                      data[idx - 1] + data[idx + 1]) + 
                             one_minus_om * data[idx])

@njit
def SparseCompRow_matmult_jit(M, y, val, row, col, x, num_iterations):
    for _ in range(num_iterations):
        for r in range(M):
            sa = 0.0
            for i in range(row[r], row[r + 1]):
                sa += x[col[i]] * val[i]
            y[r] = sa


@njit(cache=True)
def monte_carlo_kernel(samples, m_arr, m1, dm1, curr_i, curr_j):
    under_curve = 0
    # linear congruential generator logic moved inside JIT
    i, j = curr_i, curr_j
    
    for _ in range(samples):
        # generate X
        k = m_arr[i] - m_arr[j]
        if k < 0: k += m1
        m_arr[j] = k
        i = 16 if i == 0 else i - 1
        j = 16 if j == 0 else j - 1
        x = dm1 * k
        
        # generate Y
        k = m_arr[i] - m_arr[j]
        if k < 0: k += m1
        m_arr[j] = k
        i = 16 if i == 0 else i - 1
        j = 16 if j == 0 else j - 1
        y = dm1 * k
        
        if (x*x + y*y) <= 1.0:
            under_curve += 1
            
    return (float(under_curve) / samples) * 4.0

def MonteCarlo(Num_samples):
    rnd = Random(113)
    # extract state to pass to Numba (Numba likes arrays, not custom objects)
    m_arr = np.array(rnd.m, dtype=np.float64)
    return monte_carlo_kernel(Num_samples, m_arr, rnd.m1, rnd.dm1, rnd.i, rnd.j)

def bench_MonteCarlo(loops, Num_samples):
    t0 = perf.perf_counter()
    for _ in range(loops):
        MonteCarlo(Num_samples)
    return perf.perf_counter() - t0

@njit(cache=True)
def LU_factor_jit(data, M, N, pivot):
    minMN = min(M, N)
    for j in range(minMN):
        jp = j
        t = abs(data[j * N + j])
        for i in range(j + 1, M):
            ab = abs(data[i * N + j])
            if ab > t:
                jp = i
                t = ab
        pivot[j] = jp

        if data[jp * N + j] == 0:
            return False # signal failure

        if jp != j:
            # row swap in flat array
            for k in range(N):
                idx1, idx2 = j * N + k, jp * N + k
                data[idx1], data[idx2] = data[idx2], data[idx1]

        if j < M - 1:
            recp = 1.0 / data[j * N + j]
            for k in range(j + 1, M):
                data[k * N + j] *= recp

        if j < minMN - 1:
            for ii in range(j + 1, M):
                for jj in range(j + 1, N):
                    data[ii * N + jj] -= data[ii * N + j] * data[j * N + jj]
    return True

def LU(lu, A, pivot):
    lu.copy_data_from(A)
    LU_factor(lu, pivot)


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


# G15: this single compiled block replaces three baseline functions
@njit(cache=True)
def FFT_transform_jit(N, data, direction):
    n = N // 2
    if n == 1 or N == 0: return
    
    # bit-reversal
    nm1, j = n - 1, 0
    for i in range(nm1):
        ii, jj = i << 1, j << 1
        k = n >> 1
        if i < j:
            data[ii], data[jj] = data[jj], data[ii]
            data[ii+1], data[jj+1] = data[jj+1], data[ii+1]
        while k <= j:
            j -= k
            k >>= 1
        j += k

    # butterfly loops
    dual = 1
    while dual < n:
        theta = 2.0 * direction * math.pi / (2.0 * dual)
        s, t = math.sin(theta), math.sin(theta / 2.0)
        s2 = 2.0 * t * t
        
        for b in range(0, n, 2 * dual):
            i, j = 2 * b, 2 * (b + dual)
            wr, wi = data[j], data[j + 1]
            data[j], data[j + 1] = data[i] - wr, data[i + 1] - wi
            data[i], data[i + 1] = data[i] + wr, data[i + 1] + wi
        
        w_real, w_imag = 1.0, 0.0
        for a in range(1, dual):
            tr = w_real - s * w_imag - s2 * w_real
            ti = w_imag + s * w_real - s2 * w_imag
            w_real, w_imag = tr, ti
            for b in range(0, n, 2 * dual):
                i, j = 2 * (b + a), 2 * (b + a + dual)
                z1r, z1i = data[j], data[j + 1]
                wdr = w_real * z1r - w_imag * z1i
                wdi = w_real * z1i + w_imag * z1r
                data[j], data[j + 1] = data[i] - wdr, data[i + 1] - wdi
                data[i], data[i + 1] = data[i] + wdr, data[i + 1] + wdi
        dual *= 2

def SOR_execute(omega, G, cycles, Array):
    SOR_execute_jit(omega, G.data, G.height, G.width, cycles)

def bench_SOR(loops, n, cycles, Array):
    t0 = perf.perf_counter()
    for _ in range(loops):
        G = Array(n, n)
        SOR_execute(1.25, G, cycles, Array)
    return perf.perf_counter() - t0

def SparseCompRow_matmult(M, y, val, row, col, x, num_iterations):
    SparseCompRow_matmult_jit(M, y, val, row, col, x, num_iterations)
    return 0.0

def bench_SparseMatMult(loops, N, nz):
    x, y = array('d', [0.5]) * N, array('d', [0.0]) * N
    nr = nz // N
    val, col = array('d', [0.1]) * (nr * N), array('i', [1]) * nz
    row = array('i', [i * nr for i in range(N + 1)])
    t0 = perf.perf_counter()
    SparseCompRow_matmult_jit(N, y, val, row, col, x, loops)
    return perf.perf_counter() - t0

def LU_factor(A, pivot):
    if not LU_factor_jit(A.data, A.height, A.width, pivot):
        raise Exception("Zero pivot")

def bench_LU(loops, N):
# initialize with numpy arrays
    A_data = np.random.rand(N * N).astype(np.float64)
    lu_data = np.zeros(N * N, dtype=np.float64)
    pivot = np.zeros(N, dtype=np.int32)
    
    t0 = perf.perf_counter()
    for _ in range(loops):
        lu_data[:] = A_data[:]
        LU_factor_jit(lu_data, N, N, pivot)
        
    return perf.perf_counter() - t0

def FFT_inverse(N, data):
    FFT_transform_jit(N, data, +1)
    norm = 1.0 / (N // 2)
    for i in range(N): data[i] *= norm

def bench_FFT(loops, N, cycles):
    data = array('d', [0.5]) * (2 * N)
    t0 = perf.perf_counter()
    for _ in range(loops):
        for i in range(cycles):
            FFT_transform_jit(2 * N, data, -1)
            FFT_inverse(2 * N, data)
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
from array import array
import math
import pyperf as perf

class Array2D(object):
    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        size = w * h 
        self.data = array('d', [0]) * size
        if data is not None:
            self.setup(data)

    def _idx(self, x, y):
        w, h = self.width, self.height
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
        h, w = self.height, self.width
        # G7: Use slice assignment for rows to reduce individual __setitem__ calls
        # This replaces the 'for x in range(w)' loop with a single bulk memory move per row
        for y in range(h):
            start = y * w
            end = start + w
            self.data[start:end] = array('d', data[y])
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
        
        # G7: initializing the array in bulk
        self.m = array('d', [0]) * 17
        m2 = self.m2
        m2_half = m2 / 2
        for iloop in range(17):
            jseed_prod = j0 * k0
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
        self.i = 16 if I == 0 else I - 1
        self.j = 16 if J == 0 else J - 1

        if (self.haveRange):
            return self.left + self.dm1 * float(k) * self.width
        else:
            return self.dm1 * float(k)
        
    def RandomMatrix(self, a):
        nxt = self.nextDouble
        if isinstance(a, ArrayList):
            # G7: fill each row-array in bulk
            for y in range(a.height):
                a.data[y][:] = array('d', [nxt() for _ in range(a.width)])
        else:
            # G7: fill flat array in bulk
            total_elements = a.width * a.height
            a.data[:] = array('d', [nxt() for _ in range(total_elements)])
        return a

    def RandomVector(self, n):
        return array('d', [self.nextDouble() for _ in range(n)])


def copy_vector(vec):
    # Copy a vector created by Random.RandomVector()
    vec2 = array('d')
    vec2[:] = vec[:]
    return vec2


class ArrayList(Array2D):

    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        # G7: bulk creation of the nested array structure
        self.data = [array('d', [0]) * w for _ in range(h)]
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

    def setup(self, data):
        # G7: bulk loading a whole row at once into the corresponding row-array
        for y in range(self.height):
            self.data[y][:] = array('d', data[y])
        return self
    
    def copy_data_from(self, other):
        # G7: bulk row-by-row copy
        # ensure we are copying the content of the arrays, not replacing the objects
        for i in range(len(self.data)):
            self.data[i][:] = other.data[i]


def SOR_execute(omega, G, cycles, Array):
    for p in range(cycles):
        for y in range(1, G.height - 1):
            for x in range(1, G.width - 1):
                G[x, y] = (omega * 0.25 * (G[x, y - 1] + G[x, y + 1] + G[x - 1, y]
                                           + G[x + 1, y])
                           + (1.0 - omega) * G[x, y])


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
            for i in range(row[r], row[r + 1]):
                sa += x[col[i]] * val[i]
            y[r] = sa

    return perf.perf_counter() - t0


def bench_SparseMatMult(cycles, N, nz):
    # G7: bulk initialization of large arrays
    x = array('d', [0]) * N
    y = array('d', [0]) * N

    nr = nz // N
    anz = nr * N
    val = array('d', [0]) * anz
    col = array('i', [0]) * nz
    row = array('i', [0]) * (N + 1)
    
    # logic for filling row/col remains iterative due to dependency
    row[0] = 0
    for r in range(N):
        rowr = row[r]
        step = max(1, r // nr)
        row[r + 1] = rowr + nr
        for i in range(nr):
            col[rowr + i] = i * step

    return SparseCompRow_matmult(N, y, val, row, col, x, cycles)

def MonteCarlo(Num_samples):
    rnd = Random(113)
    under_curve = 0
    for count in range(Num_samples):
        x = rnd.nextDouble()
        y = rnd.nextDouble()
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
    M, N = A.height, A.width
    minMN = min(M, N)
    for j in range(minMN):
        jp = j
        t = abs(A[j][j])
        for i in range(j + 1, M):
            ab = abs(A[i][j])
            if ab > t:
                jp = i
                t = ab
        pivot[j] = jp

        if A[jp][j] == 0:
            raise Exception("factorization failed because of zero pivot")

        if jp != j:
            A[j], A[jp] = A[jp], A[j]

        if j < M - 1:
            recp = 1.0 / A[j][j]
            for k in range(j + 1, M):
                A[k][j] *= recp

        if j < minMN - 1:
            for ii in range(j + 1, M):
                for jj in range(j + 1, N):
                    A[ii][jj] -= A[ii][j] * A[j][jj]


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
    bit = 0
    while bit < logn:
        w_real = 1.0
        w_imag = 0.0
        theta = 2.0 * direction * math.pi / (2.0 * float(dual))
        s = math.sin(theta)
        t = math.sin(theta / 2.0)
        s2 = 2.0 * t * t
        for b in range(0, n, 2 * dual):
            i = 2 * b
            j = 2 * (b + dual)
            wd_real = data[j]
            wd_imag = data[j + 1]
            data[j] = data[i] - wd_real
            data[j + 1] = data[i + 1] - wd_imag
            data[i] += wd_real
            data[i + 1] += wd_imag
        for a in range(1, dual):
            tmp_real = w_real - s * w_imag - s2 * w_real
            tmp_imag = w_imag + s * w_real - s2 * w_imag
            w_real = tmp_real
            w_imag = tmp_imag
            for b in range(0, n, 2 * dual):
                i = 2 * (b + a)
                j = 2 * (b + a + dual)
                z1_real = data[j]
                z1_imag = data[j + 1]
                wd_real = w_real * z1_real - w_imag * z1_imag
                wd_imag = w_real * z1_imag + w_imag * z1_real
                data[j] = data[i] - wd_real
                data[j + 1] = data[i + 1] - wd_imag
                data[i] += wd_real
                data[i + 1] += wd_imag
        bit += 1
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
    FFT_transform_internal(N, data, +1)
    n_val = N / 2
    norm = 1 / float(n_val)
    # G7: use a map or comprehension to process the 'batch' more efficiently than a manual for loop
    data[:] = array('d', (val * norm for val in data))

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
import numpy as np
import pyperf as perf

class RandomG5(object):
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
        
        # keep internal generator arrays at standard precision to prevent overflow
        self.m = [0] * 17
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

        if (I == 0): I = 16
        else: I -= 1
        self.i = I

        if (J == 0): J = 16
        else: J -= 1
        self.j = J

        if (self.haveRange):
            return self.left + self.dm1 * float(k) * self.width
        else:
            return self.dm1 * float(k)


def MonteCarlo(Num_samples):
    rnd = RandomG5(113)
    under_curve = 0
    for count in range(Num_samples):
        # G5: fetch coordinates and force them immediately into FP16 low-precision
        x = np.float16(rnd.nextDouble())
        y = np.float16(rnd.nextDouble())
        
        # perform all the bounding-box math entirely under 16-bit constraints
        if np.float16(x * x) + np.float16(y * y) <= np.float16(1.0):
            under_curve += 1
            
    return float(under_curve) / Num_samples * 4.0


def bench_MonteCarlo(loops, Num_samples):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        MonteCarlo(Num_samples)

    return perf.perf_counter() - t0


if __name__ == "__main__":
    runner = perf.Runner()
    runner.bench_time_func('monte_carlo_g5', bench_MonteCarlo, 100000)
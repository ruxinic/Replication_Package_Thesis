from decimal import *
from decimal import Decimal, getcontext
import pyperf as perf

def GaussLegendreBaseline(iterations):
    D = Decimal
    getcontext().prec = 100
    a = n = D(1)
    g, z, half = 1 / D(2).sqrt(), D(0.25), D(0.5)
    for i in range(iterations):
        x = [(a + g) * half, (a * g).sqrt()]
        var = x[0] - a
        z -= var * var * n
        n += n
        a, g = x    
    return float(a * a / z)

def bench_gauss(loops, iterations):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        GaussLegendreBaseline(iterations)

    return perf.perf_counter() - t0

if __name__ == "__main__":
    runner = perf.Runner()
    # 18 iterations is the standard limit for Gauss-Legendre testing
    runner.bench_time_func('gauss_precision_baseline', bench_gauss, 10)
import numpy as np
import pyperf as perf

def GaussLegendreG5(iterations):
    # enforce low-precision 16-bit hardware profiles
    a = np.float16(1.0)
    n = np.float16(1.0)
    
    g = np.float16(1.0 / np.sqrt(np.float16(2.0)))
    z = np.float16(0.25)
    half = np.float16(0.5)
    
    # updated to use the iterations parameter dynamically
    for i in range(iterations):
        # all steps calculated under raw 16-bit hardware constraints
        sum_ag = np.float16(a + g)
        x0 = np.float16(sum_ag * half)
        x1 = np.float16(np.sqrt(np.float16(a * g)))
        
        var = np.float16(x0 - a)
        z = np.float16(z - np.float16(np.float16(var * var) * n))
        n = np.float16(n + n)
        
        a = x0
        g = x1
        
    return float(np.float16(np.float16(a * a) / z))

def bench_gauss_g5(loops, iterations):
    range_it = range(loops)
    t0 = perf.perf_counter()

    for _ in range_it:
        GaussLegendreG5(iterations)

    return perf.perf_counter() - t0

if __name__ == "__main__":
    runner = perf.Runner()
    # Passes 18 into the iterations parameter
    runner.bench_time_func('gauss_g5_approximate', bench_gauss_g5, 10)
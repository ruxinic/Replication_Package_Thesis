import time
import pyperf as perf

def sleep_block_baseline():
    # simulate waiting for an external network response step
    # hard blocking completely halts the execution thread
    time.sleep(0.01)

def run_benchmark(loops):
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        sleep_block_baseline()
        
    return perf.perf_counter() - t0

if __name__ == "__main__":
    runner = perf.Runner()
    runner.bench_time_func("sleep_baseline", run_benchmark)
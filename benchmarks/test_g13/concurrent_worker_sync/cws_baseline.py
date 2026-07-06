import time
import pyperf as perf

def sequential_worker():
    # simulate a small I/O latency delay
    time.sleep(0.01)

def run_workers_baseline(num_workers):
    # processing 100 concurrent I/O operations sequentially
    # The CPU thread completely freezes for 0.01s, 100 separate times in a row
    for _ in range(num_workers):
        sequential_worker()

def run_benchmark(loops):
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        # pass 100 workers to force a noticeable blocking window
        run_workers_baseline(100)
        
    return perf.perf_counter() - t0

if __name__ == "__main__":
    runner = perf.Runner()
    
    # force pyperf to bypass its auto-calibration and use our exact loop count
    cmd = runner.parse_args()
    if cmd.loops is None:
        # 5 loops * (100 workers * 0.01s) = Exactly 5.0 seconds of sequential execution
        cmd.loops = 10  
        
    runner.bench_time_func("b3_concurrency_baseline", run_benchmark)
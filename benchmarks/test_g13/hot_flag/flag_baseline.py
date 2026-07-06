import time
import pyperf as perf

class SimulatedProcess:
    def __init__(self):
        self.start_time = time.perf_counter()
        
    def is_finished(self):
        # the event finishes after exactly 0.1 seconds
        return (time.perf_counter() - self.start_time) >= 0.1

def wait_for_event_baseline(process):
    # active loop spins at maximum possible speed,
    # pegging the CPU core to 100% load while checking the flag status
    while not process.is_finished():
        pass

def run_benchmark(loops):
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        process = SimulatedProcess()
        wait_for_event_baseline(process)
        
    return perf.perf_counter() - t0

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        # 20 loops * 0.1s delay = ~2 seconds of high-power CPU spinning
        cmd.loops = 20  
        
    runner.bench_time_func("b4_event_polling_baseline", run_benchmark)
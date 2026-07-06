import asyncio
import time
import pyperf as perf

class SimulatedProcess:
    def __init__(self):
        self.start_time = time.perf_counter()
        
    def is_finished(self):
        return (time.perf_counter() - self.start_time) >= 0.1

async def wait_for_event_g13(process):
    # G13: instead of pinning the thread, we back off
    # the coroutine sleeps non-actively, freeing hardware resources
    while not process.is_finished():
        await asyncio.sleep(0.005)

async def main_loop(loops):
    for _ in range(loops):
        process = SimulatedProcess()
        await wait_for_event_g13(process)

def run_benchmark(loops):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    t0 = perf.perf_counter()
    loop.run_until_complete(main_loop(loops))
    duration = perf.perf_counter() - t0
    
    loop.close()
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        cmd.loops = 20  
        
    runner.bench_time_func("b4_event_polling_g13", run_benchmark)
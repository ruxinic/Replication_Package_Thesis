import asyncio
import pyperf as perf

async def concurrent_worker_g13():
    # G13: suspends the task immediately, freeing resources
    await asyncio.sleep(0.01)

async def run_workers_g13(num_workers):
    # prepare 100 worker tasks to run at the same time
    tasks = [concurrent_worker_g13() for _ in range(num_workers)]
    
    # G13: the thread sleeps once for the entire cluster of tasks
    await asyncio.gather(*tasks)

def run_benchmark(loops):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        # fire off 100 concurrent worker tasks per loop iteration
        loop.run_until_complete(run_workers_g13(num_workers=100))
        
    duration = perf.perf_counter() - t0
    loop.close()
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        cmd.loops = 10
        
    runner.bench_time_func("b3_concurrency_g13", run_benchmark)
import asyncio
import pyperf as perf

async def sleep_block_g13():
    # the coroutine enters a non-active, resource-free Sleep state
    await asyncio.sleep(0.01)

def run_benchmark(loops):
    # establish the event loop runner
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        loop.run_until_complete(sleep_block_g13())
        
    duration = perf.perf_counter() - t0
    loop.close()
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    runner.bench_time_func("sleep_g13", run_benchmark)
import asyncio
import os
import pyperf as perf

def synchronous_io_worker(filename, data):
    with open(filename, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    with open(filename, "rb") as f:
        _ = f.read()

async def disk_operations_g13(filename, data):
    # G13: delegate blocking storage actions to a background thread
    # main loop yields immediately, remaining non-blocking and responsive
    await asyncio.to_thread(synchronous_io_worker, filename, data)

async def main_loop(loops, filename, payload):
    for _ in range(loops):
        await disk_operations_g13(filename, payload)

def run_benchmark(loops):
    filename = "test_b5_g13.tmp"
    payload = b"X" * (5 * 1024 * 1024)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    t0 = perf.perf_counter()
    loop.run_until_complete(main_loop(loops, filename, payload))
    duration = perf.perf_counter() - t0
    
    loop.close()
    
    if os.path.exists(filename):
        os.remove(filename)
        
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        cmd.loops = 15  
        
    runner.bench_time_func("b5_disk_io_g13", run_benchmark)

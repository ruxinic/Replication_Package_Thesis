import asyncio
import pyperf as perf

async def receive_data_g13(queue):
    # G13: the execution frame suspends completely here
    # the process drops into a sleep state, using 0% CPU while waiting for the item
    data = await queue.get()
    queue.task_done()
    return data

async def delayed_sender(queue):
    await asyncio.sleep(0.001)
    await queue.put(b"data")

async def main_loop(loops, queue):
    for _ in range(loops):
        # fire off the asynchronous sender task concurrently
        sender_task = asyncio.create_task(delayed_sender(queue))
        
        # read the data while non-actively sleeping
        await receive_data_g13(queue)
        
        # ensure the sender task is fully completed before moving on
        await sender_task

def run_benchmark(loops):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # use a pure-async queue buffer to bypass OS-specific socket bugs
    queue = asyncio.Queue()
    
    t0 = perf.perf_counter()
    loop.run_until_complete(main_loop(loops, queue))
    duration = perf.perf_counter() - t0
    
    loop.close()
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        cmd.loops = 2000  
        
    runner.bench_time_func("b2_socket_polling_g13", run_benchmark)
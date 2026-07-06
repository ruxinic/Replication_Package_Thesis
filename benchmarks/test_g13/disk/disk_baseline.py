import os
import pyperf as perf

def disk_operations_baseline(filename, data):
    # main thread directly performs synchronous blocking file I/O
    # the CPU core is forced to block completely while waiting for the disk hardware
    with open(filename, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())  # force OS buffer write to physical storage

    with open(filename, "rb") as f:
        _ = f.read()

def run_benchmark(loops):
    filename = "test_b5_baseline.tmp"
    # create a 5MB data block to ensure measurable disk operations
    payload = b"X" * (5 * 1024 * 1024)
    
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        disk_operations_baseline(filename, payload)
        
    duration = perf.perf_counter() - t0
    
    if os.path.exists(filename):
        os.remove(filename)
        
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        # 15 loops writing/reading 5MB blocks forces a sustained disk-blocking load
        cmd.loops = 15  
        
    runner.bench_time_func("b5_disk_io_baseline", run_benchmark)
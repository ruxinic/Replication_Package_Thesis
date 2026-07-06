import socket
import threading
import time
import pyperf as perf

def receive_data_baseline(sock_rx):
    # continuous polling loop burns CPU cycles doing nothing
    while True:
        try:
            data = sock_rx.recv(1024)
            if data:
                return data
        except BlockingIOError:
            # buffer is truly empty now!
            # rushing back to check instantly spikes CPU core to 100%
            continue

def delayed_sender(sock_tx):
    # deliberately sleep for 1 millisecond to force the receiver to busy-wait
    time.sleep(0.001)
    sock_tx.send(b"data")

def run_benchmark(loops):
    sock_tx, sock_rx = socket.socketpair()
    sock_rx.setblocking(False)  # non-blocking to allow polling
    
    t0 = perf.perf_counter()
    
    for _ in range(loops):
        # start the sender on a background thread with a delay
        sender_thread = threading.Thread(target=delayed_sender, args=(sock_tx,))
        sender_thread.start()
        
        # main thread is trapped here, spinning wildly until data arrives
        receive_data_baseline(sock_rx)
        
        # clean up the thread before the next loop
        sender_thread.join()
        
    duration = perf.perf_counter() - t0
    sock_tx.close()
    sock_rx.close()
    return duration

if __name__ == "__main__":
    runner = perf.Runner()
    
    cmd = runner.parse_args()
    if cmd.loops is None:
        # 2000 loops * 0.001s delay = ~2 seconds of high-fidelity, 100% CPU energy
        cmd.loops = 2000  
        
    runner.bench_time_func("b2_socket_polling_baseline", run_benchmark)
import time

def check_condition():
    return time.time() > start_time + 8

start_time = time.time()

# G13: Use sleep state while waiting
while not check_condition():
    # Giving the CPU a break (100ms) significantly reduces energy
    time.sleep(0.1) 

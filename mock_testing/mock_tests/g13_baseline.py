import time

def check_condition():
    # Simulate waiting for a specific time to pass
    return time.time() > start_time + 8

start_time = time.time()

# Busy Waiting
# The CPU is spinning at 100% usage doing nothing useful
while not check_condition():
    pass 

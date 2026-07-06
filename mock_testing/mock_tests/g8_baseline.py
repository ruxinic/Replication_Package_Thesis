import threading
import math

def python_heavy_task(n):
    result = 0
    for i in range(n):
        result += math.sqrt(i)

# 2 threads running Python code (GIL bottleneck)
n = 10_000_000
t1 = threading.Thread(target=python_heavy_task, args=(n,))
t2 = threading.Thread(target=python_heavy_task, args=(n,))

t1.start(); t2.start()
t1.join(); t2.join()
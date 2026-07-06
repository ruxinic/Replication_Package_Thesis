import numpy as np

# Use standard 64-bit precision for the baseline
dtype = np.float64

f = lambda x: x * x * x - 3 * x * x + 2 * x

step = dtype(0.001)
start = dtype(-1)
stop = dtype(3)

sign = f(start) > 0
x = start
root_count = 0

while x <= stop:
    value = f(x)

    if value == 0:
        print(f"Root found at {float(x):.4f}")
        root_count += 1
    elif (value > 0) != sign:
        print(f"Root found near {float(x):.4f}")
        root_count += 1

    sign = value > 0
    x += step

print(f"Total Root Indications Found: {root_count}")
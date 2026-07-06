def loop_optimized(data):
    i = 0
    # G3: Storing loop end condition in a variable
    n = len(data) 
    
    while i < n:
        _ = data[i] ** 2
        i += 1
    return True

large_data = list(range(10000))
loop_optimized(large_data)
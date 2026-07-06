def loop_baseline(data):
    i = 0
    # The end condition len(data) is re-evaluated every iteration
    while i < len(data):
        _ = data[i] ** 2
        i += 1
    return True

large_data = list(range(10000))
loop_baseline(large_data)
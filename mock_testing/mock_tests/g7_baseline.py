import random

def generate_data_baseline(n):
    data = []
    # Handling tasks individually in a loop
    for _ in range(n):
        data.append(random.randint(1, 100))
    return data

generate_data_baseline(1000000)
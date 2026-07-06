# Simulation of a large coordinate dataset
large_dataset = [(i, i * 1.5) for i in range(5_000_000)]

class PointProcessor:
    def __init__(self, ox, oy):
        self.offset_x = ox
        self.offset_y = oy

    def transform(self, x, y):
        # Function call overhead + attribute lookup on 'self'
        return x + self.offset_x, y + self.offset_y

def run_baseline():
    processor = PointProcessor(10.5, 20.5)
    results = []
    
    # Measuring this loop
    for x, y in large_dataset:
        results.append(processor.transform(x, y))
    
    return results

if __name__ == "__main__":
    run_baseline()

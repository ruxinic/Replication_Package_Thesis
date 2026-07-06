# Simulation of a large coordinate dataset
large_dataset = [(i, i * 1.5) for i in range(5_000_000)]

class PointProcessor:
    def __init__(self, ox, oy):
        self.offset_x = ox
        self.offset_y = oy

def run_optimized():
    processor = PointProcessor(10.5, 20.5)
    
    # Pre-fetch attributes to local variables (Avoids repeated lookups)
    ox = processor.offset_x
    oy = processor.offset_y
    results = []
    
    # Measuring this loop (Inlined logic)
    for x, y in large_dataset:
        results.append((x + ox, y + oy))
    
    return results

if __name__ == "__main__":
    run_optimized()

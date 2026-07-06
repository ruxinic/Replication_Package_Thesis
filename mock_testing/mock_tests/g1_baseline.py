import math
import sys

def main(n):
    total = 0
    for i in range(n):
        total += (math.sqrt(i) * math.pi) + (math.sqrt(i) * math.pi)
        total -= (math.sqrt(i) * math.pi) / 2
        total += (math.sqrt(i) * math.pi) * 0.1
    print(total)

if __name__ == "__main__":
    # N should be large enough to run for at least 1-2 seconds 
    # so EnergiBridge can capture enough data points.
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000000
    main(N)
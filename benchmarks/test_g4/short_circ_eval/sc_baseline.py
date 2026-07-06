import sys

def a(answer):
    return answer

def b(answer):
    return answer

def run_experiment(iterations):
    for _ in range(iterations):
        for i in (False, True):
            for j in (False, True):
                # BASELINE (Eager Evaluation) but we changed and to & and or to | for the purpose of this experiment
                # Both functions must be evaluated entirely to compute the bitwise outcome
                x = a(i) & b(j)
                y = a(i) | b(j)

if __name__ == "__main__":
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 50000000
    run_experiment(iters)
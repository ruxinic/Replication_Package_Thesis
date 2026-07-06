import sys

def a(answer):
    return answer

def b(answer):
    return answer

def run_experiment(iterations):
    for _ in range(iterations):
        for i in (False, True):
            for j in (False, True):
                # this is actuallt how it is written on rosetta code 
                # function b(j) is bypassed whenever a(i) is sufficient
                x = a(i) and b(j)
                y = a(i) or b(j)

if __name__ == "__main__":
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 50000000
    run_experiment(iters)
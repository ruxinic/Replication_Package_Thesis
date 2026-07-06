import sys
import cupy as cp

def main(N):
    X = cp.linspace(-2.0, 0.5, N)
    Y = cp.linspace(-1.0, 1.0, N)
    C = X[cp.newaxis, :] + 1j * Y[:, cp.newaxis] # full complex grid

    Z = cp.zeros_like(C)
    out = cp.zeros(C.shape, dtype=cp.int32) # escape iteration per pixel
    alive = cp.ones(C.shape, dtype=bool) # pixels not yet escaped

    # mirrors the baseline's `for n in range(1, 100)`
    for n in range(1, 100):
        Z[alive] = Z[alive] ** 2 + C[alive]
        escaped = alive & (cp.abs(Z) > 2.0)
        out[escaped] = n # record escape iteration; non-escaped stay 0
        alive &= ~escaped
        if not bool(alive.any()): # all pixels escaped means done early
            break

    result = int(out.sum())
    cp.cuda.Stream.null.synchronize() # finish GPU work before timer ends
    return result

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    print(f"Checksum: {main(N)}")
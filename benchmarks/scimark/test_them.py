import math
import numpy as np
import scimark_baseline as base
import scimark_g1 as g1
import scimark_g3 as g3
import scimark_g7 as g7
import scimark_g19 as g19
import scimark_g15 as g15
import scimark_g24 as g24
# previous version (outdated)
def verify_all():
    EPSILON = 1e-12
    print("--- Starting Global Consistency Verification ---")

    # --- 1. Monte Carlo ---
    samples = 100000
    results_mc = {
        "Base": base.MonteCarlo(samples),
        "G1":   g1.MonteCarlo(samples),
        "G3":   g3.MonteCarlo(samples),
        "G7":   g7.MonteCarlo(samples),
        "G19":  g19.MonteCarlo(samples),
        "G15":  g15.MonteCarlo(samples),
        "G24":  g24.MonteCarlo(samples)
    }
    
    for name, val in results_mc.items():
        if name != "Base":
            assert math.isclose(results_mc["Base"], val, abs_tol=EPSILON), f"MC {name} Mismatch"
    print("Monte Carlo: All versions consistent.")

    # --- 2. FFT ---
    N_fft = 1024
    size = 2 * N_fft
    init_data = [float(i) for i in range(size)]

    # transform functions vary in signature slightly between versions
    # Base/G1/G3/G7/G19 usually use list/array in-place
    # G15 uses numpy in-place
    versions_fft = {
        "G1":   (g1.FFT_transform, list(init_data)),
        "G3":   (g3.FFT_transform, list(init_data)),
        "G7":   (g7.FFT_transform, list(init_data)),
        "G19":  (g19.FFT_transform, list(init_data)),
        "G15":  (g15.FFT_transform_jit, np.array(init_data, dtype=np.float64)),
        "G24":  (g24.FFT_transform, list(init_data))

    }

    # get Baseline reference
    base_data = list(init_data)
    base.FFT_transform(size, base_data)

    for name, (func, data) in versions_fft.items():
        if name == "G15":
            func(size, data, -1) # G15 usually requires the direction parameter
        else:
            func(size, data)
        assert np.allclose(base_data, data, atol=1e-10), f"FFT {name} Mismatch"
    print("FFT: All versions consistent.")

    # --- 3. SOR ---
    N_sor = 100
    cycles = 10
    # baseline SOR usually takes (omega, G, cycles, ArrayClass)
    # optimized SOR often takes (omega, G, cycles)
    
    # We compare by summing the final grid data
    G_base = base.Array2D(N_sor, N_sor)
    base.SOR_execute(1.25, G_base, cycles, base.Array2D)
    ref_sum = sum(G_base.data)

    # test G19 and G15 specifically (as they usually have the most logic changes)
    G_19 = g19.Array2D(N_sor, N_sor)
    g19.SOR_execute(1.25, G_19, cycles) # call matching optimized G19 signature
    
    G_15 = g15.Array2D(N_sor, N_sor)
    g15.SOR_execute(1.25, G_15, cycles, g15.Array2D)

    assert math.isclose(ref_sum, sum(G_19.data), rel_tol=EPSILON), "SOR G19 Mismatch"
    assert math.isclose(ref_sum, sum(G_15.data), rel_tol=EPSILON), "SOR G15 Mismatch"
    print("SOR: Optimized versions consistent.")

# --- 4. Sparse MatMult ---
    N_sp = 100
    nz = 1000
    # Create identical inputs
    x = np.array([0.5] * N_sp, dtype=np.float64)
    val = np.array([0.1] * nz, dtype=np.float64)
    col = np.array([i % N_sp for i in range(nz)], dtype=np.int32)
    row = np.array([i * (nz // N_sp) for i in range(N_sp + 1)], dtype=np.int32)
    
    # Baseline Result
    y_base = np.zeros(N_sp, dtype=np.float64)
    base.SparseCompRow_matmult(N_sp, y_base, val, row, col, x, 1)

    # G19 Result
    y_g19 = np.zeros(N_sp, dtype=np.float64)
    g19.SparseCompRow_matmult(N_sp, y_g19, val, row, col, x, 1)

    # G15 Result
    y_g15 = np.zeros(N_sp, dtype=np.float64)
    g15.SparseCompRow_matmult_jit(N_sp, y_g15, val, row, col, x, 1)

    assert np.allclose(y_base, y_g19, atol=EPSILON), "Sparse G19 Mismatch"
    assert np.allclose(y_base, y_g15, atol=EPSILON), "Sparse G15 Mismatch"
    print(" Sparse MatMult: All versions consistent.")

    # --- 5. LU Factorization ---
    N_lu = 16
    # seed a random matrix for testing
    rnd = base.Random(42)
    matrix_data = [[rnd.nextDouble() for _ in range(N_lu)] for _ in range(N_lu)]
    
    # baseline
    A_base = base.ArrayList(N_lu, N_lu, data=matrix_data)
    pivot_base = [0] * N_lu
    base.LU_factor(A_base, pivot_base)
    # sum the factored matrix to create a unique fingerprint
    base_check = sum(sum(row) for row in A_base.data)

    # G19 (Standard ArrayList path)
    A_g19 = g19.ArrayList(N_lu, N_lu, data=matrix_data)
    pivot_g19 = [0] * N_lu
    g19.LU_factor(A_g19, pivot_g19)
    g19_check = sum(sum(row) for row in A_g19.data)

    # G15 (Flattened JIT path)
    # G15 uses flat arrays for JIT, so we flatten matrix_data
    flat_data = np.array([item for sublist in matrix_data for item in sublist], dtype=np.float64)
    pivot_g15 = np.zeros(N_lu, dtype=np.int32)
    g15.LU_factor_jit(flat_data, N_lu, N_lu, pivot_g15)
    g15_check = np.sum(flat_data)

    assert math.isclose(base_check, g19_check, rel_tol=1e-10), "LU G19 Mismatch"
    assert math.isclose(base_check, g15_check, rel_tol=1e-10), "LU G15 Mismatch"
    print("LU: All versions consistent.")

    print("\ ALL VERSIONS PASSED CONSISTENCY CHECKS")

if __name__ == "__main__":
    verify_all()
import sys
import os
import numpy as np
import polars as pl
import pyperf as perf

def compute_mandelbrot_g27(parquet_file, num_iterations=99):
    # G27: load the coordinate grid into memory via a parallel scan
    lazy_df = pl.scan_parquet(parquet_file)
    
    # initialize the tracking columns (Z_real and Z_imag start at 0)
    lazy_df = lazy_df.with_columns([
        pl.lit(0.0).alias("z_r"),
        pl.lit(0.0).alias("z_i"),
        pl.lit(0).alias("escape_iter")
    ])
    
    # run the escape-time loop over all columns concurrently
    for n in range(1, num_iterations + 1):
        # Mandelbrot formula split into real/imaginary parts: 
        # Z_next = Z^2 + C -> (r^2 - i^2 + c_r) + i*(2*r*i + c_i)
        lazy_df = lazy_df.with_columns([
            (pl.col("z_r") * pl.col("z_r") - pl.col("z_i") * pl.col("z_i") + pl.col("c_r")).alias("next_z_r"),
            (2.0 * pl.col("z_r") * pl.col("z_i") + pl.col("c_i")).alias("next_z_i")
        ]).with_columns([
            # check if magnitude squared > 4 (equivalent to abs(z) > 2)
            pl.when(
                (pl.col("escape_iter") == 0) & 
                ((pl.col("next_z_r") * pl.col("next_z_r") + pl.col("next_z_i") * pl.col("next_z_i")) > 4.0)
            )
            .then(pl.lit(n))
            .otherwise(pl.col("escape_iter"))
            .alias("escape_iter"),
            
            pl.col("next_z_r").alias("z_r"),
            pl.col("next_z_i").alias("z_i")
        ])
        
    # flush computation across all underlying CPU threads
    result = lazy_df.select("escape_iter").collect()
    return int(result["escape_iter"].sum())

def bench_mandelbrot(N):
    # setup the coordinate matrix space
    X = np.linspace(-2, 0.5, N)
    Y = np.linspace(-1, 1, N)
    
    # flat map the 2D grid into a relational, columnar format
    c_real_list = []
    c_imag_list = []
    for y in Y:
        for x in X:
            c_real_list.append(float(x))
            c_imag_list.append(float(y))
            
    # pack elements into a structural Polars Dataframe
    df = pl.DataFrame({
        "c_r": c_real_list,
        "c_i": c_imag_list
    })
    
    # cache to disk as Parquet to complete the G27 storage architecture pipeline
    parquet_filename = "mandelbrot_g27.parquet"
    df.write_parquet(parquet_filename)
    
    # execute and time the core engine loop
    t0 = perf.perf_counter()
    checksum = compute_mandelbrot_g27(parquet_filename)
    duration = perf.perf_counter() - t0
    
    # clean up disk file
    if os.path.exists(parquet_filename):
        os.remove(parquet_filename)
        
    print(f"Checksum: {checksum}")
    return duration

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    duration = bench_mandelbrot(N)

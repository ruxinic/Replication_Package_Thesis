#include <stdlib.h>
#include <math.h>

// computes the escape time iteration for a single complex coordinate point
int compute_pixel(double cr, double ci, int max_iter) {
    double zr = 0.0;
    double zi = 0.0;
    
    for (int n = 1; n < max_iter; n++) {
        // force exact bitwise alignment with Python's abs(z) > 2
        // using the exact same underlying C hypot library function
        if (hypot(zr, zi) > 2.0) {
            return n;
        }
        
        double next_zi = 2.0 * zr * zi + ci;
        double next_zr = (zr * zr) - (zi * zi) + cr;
        
        zr = next_zr;
        zi = next_zi;
    }
    return 0;
}
// processes the entire 2D matrix layout completely in local hardware memory
void compute_mandelbrot(int width, int height, const double* X, const double* Y, double* Z) {
    for (int iy = 0; iy < height; iy++) {
        double y_val = Y[iy];
        long long row_offset = (long long)iy * width;
        
        for (int ix = 0; ix < width; ix++) {
            double x_val = X[ix];
            Z[row_offset + ix] = (double)compute_pixel(x_val, y_val, 100);
        }
    }
}
#include <stdlib.h>
// pure C translation of the mathematical matrix element generator
inline double eval_A(int i, int j) {
    int ij = i + j;
    return 1.0 / (ij * (ij + 1) / 2 + i + 1);
}
// compute the A matrix multiplication over the input array
void multiply_Av(int n, const double* u, double* out) {
    for (int i = 0; i < n; i++) {
        double sum = 0.0;
        for (int j = 0; j < n; j++) {
            sum += eval_A(i, j) * u[j];
        }
        out[i] = sum;
    }
}
// compute the Transposed A matrix multiplication over the input array
void multiply_Atv(int n, const double* u, double* out) {
    for (int i = 0; i < n; i++) {
        double sum = 0.0;
        for (int j = 0; j < n; j++) {
            sum += eval_A(j, i) * u[j];
        }
        out[i] = sum;
    }
}
// combine both operations to execute At * A * v entirely in C memory space
void multiply_AtAv(int n, const double* u, double* out, double* tmp) {
    multiply_Av(n, u, tmp);
    multiply_Atv(n, tmp, out);
}
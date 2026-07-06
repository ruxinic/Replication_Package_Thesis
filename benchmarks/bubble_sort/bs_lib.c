#include <stdlib.h>

void compute_bubble_sort(long long* arr, int size) {
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int i = 0; i < size - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                // Swap the values cleanly
                long long temp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = temp;
                changed = 1;
            }
        }
    }
}
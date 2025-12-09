#include "stdbool.h"
extern void svf_assert(bool);
extern int rand(int, int);

int main() {
    int a = rand(0, 20);
    int b = 0;
    if (a < 5 && a > 10) {
        b = 8;
    }
    svf_assert(b == 8);
    return 0;
}
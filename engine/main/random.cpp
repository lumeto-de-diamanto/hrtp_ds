#include "nds/ndstypes.h"
#include "random.hpp"

// XORWOW implementation from Wikipedia

static uint32 x[5];
static uint32 counter;

void initialize_irand(uint32 seed) {
    x[0] = seed;
    // Can't have all of them be zero!
    x[1] = 1;
    x[2] = 4;
    x[3] = 9;
    x[4] = 16;
    counter = 25;
}

int irand() {
    uint32_t t = x[4];

    uint32_t s = x[0]; // Perform a contrived 32-bit rotate.
    x[4] = x[3];
    x[3] = x[2];
    x[2] = x[1];
    x[1] = s;

    t ^= t >> 2;
    t ^= t << 1;
    t ^= s ^ (s << 4);

    x[0] = t;
    counter += 362437;
    return t + counter;
}
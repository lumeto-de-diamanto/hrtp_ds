#include "background.hpp"
#include "nds/arm9/background.h"
#include <nds.h>

#include "backgrounds/st0.h"

#include "file_load.c"

void load_background(StageBackground background) {
    int bg = bgInitHidden(3, BgType_Bmp8, BgSize_B8_256x256, 0, 0);
    void *bin_buf; void *pal_buf;
    size_t bin_size; size_t pal_size;
    char* file_name;
    switch (background) {
        case BG_STAGE_0:
            pal_buf = const_cast<short unsigned*>(st0_palette);
            pal_size = sizeof(st0_palette);
            file_name = "nitro:/st0.bin";
        break;
    }
    if (!file_load(file_name, &bin_buf, &bin_size))
    {
        printf("Error opening file!");
    }
    memcpy(BG_PALETTE, pal_buf, pal_size);
    memcpy(bgGetGfxPtr(bg), bin_buf, bin_size);
    bgShow(bg);
}
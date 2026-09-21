#include "orb_render.hpp"
#include "main/player/orb.hpp"
#include <nds.h>

#include "sprites/Orb.h"

const int FRAME_H = 16;
const int FRAME_W = 16;

const int FRAME_COUNT = 4;

const int FRAME_BYTES = (FRAME_H * FRAME_W * 4) / 8;

u16 *g_orb_gfx[FRAME_COUNT];

void orb_render_init(void)
{
    const uint8_t *tiles_bytes = reinterpret_cast<const uint8_t *>(Orb_tiles);

    for (int i = 0; i < FRAME_COUNT; i++)
    {
        g_orb_gfx[i] = oamAllocateGfx(&oamMain, SpriteSize_16x16,
                                         SpriteColorFormat_16Color);
        memcpy(g_orb_gfx[i], tiles_bytes + (i * FRAME_BYTES),
               FRAME_BYTES);
    }

    // Uses the same palette as Reimu
    // memcpy(SPRITE_PALETTE + 32, Orb_palette, sizeof(Orb_palette));
}

void orb_render_frame() {
    const OrbState &state = orb_get_state();
    oamSet(&oamMain, 10,
               state.x_position / 2, state.y_position / 2,
               0, 0, // priority, palette bank 1
               SpriteSize_16x16, SpriteColorFormat_16Color,
               g_orb_gfx[state.sprite_number],
               -1, false,
               false, // not hidden
               false, false, false);
}
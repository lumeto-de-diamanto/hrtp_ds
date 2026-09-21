#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <filesystem.h>
#include <main/random.hpp>

#include "background.hpp"

#include <main/player/player.hpp>
#include <main/player/shot.hpp>
#include <main/player/orb.hpp>

#include "nds/arm9/video.h"
#include "player_render.hpp"
#include "shot_render.hpp"
#include "orb_render.hpp"

#include <nds.h>

int main(int argc, char **argv)
{
    if (!nitroFSInit(NULL))
    {
        // Initialize console
        consoleDemoInit();
        // Print string followed by the cause of the error
        perror("NitroFS init error!");
        while (1)
            swiWaitForVBlank();
    }

    initialize_irand(time(NULL));

    videoSetMode(MODE_5_2D);
    vramSetPrimaryBanks(VRAM_A_MAIN_BG, VRAM_B_MAIN_SPRITE, VRAM_C_LCD,
                         VRAM_D_LCD);

    oamInit(&oamMain, SpriteMapping_1D_32, false);

    consoleDemoInit();
    printf("DEMO\n");
    printf("LEFT, RIGHT: Move Reimu\n");
    printf("A: Swing gohei\n");
    printf("B: Shoot ofuda\n\n");
    printf("START: exit to loader\n\n");

    load_background(BG_STAGE_0);

    player_initialize();
    shots_initialize();
    orb_initialize();

    player_render_init();
    shots_render_init();
    orb_render_init();

    while (1)
    {
        swiWaitForVBlank();

        scanKeys();
        uint16_t keys_held = keysHeld();
        uint16_t keys_down = keysDown();

        if (keys_held & KEY_START)
            break;

        player_update(keys_held, keys_down);
        shots_update();
        orb_update();

        player_render_frame();
        shots_render_frame();
        orb_render_frame();

        oamUpdate(&oamMain);
    }

    return 0;
}

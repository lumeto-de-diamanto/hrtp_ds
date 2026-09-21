# Port architectural plans

These plans are a work-in-progress, and are subject to change.

## Graphics

Most graphics will be halved in size, though different scaling will be used for some images, e.g. YuugenMagan and the endings.

### Stage backgrounds

The stage backgrounds will be rendered with 256-color bitmaps, with the color averaged over each 2x2 area - the result is quite nice and DS-y. The halved image is then cropped to the bottom middle 256×192 area.

**TODO**: How to handle YuugenMagan's sheer size

### Ending images

**TODO**: Scale each image down to 256×160 and letterbox?

### Gameplay graphics

During regular gameplay, the screen will be rendered using Mode 5, with BG2 placed in front of BG1 with `bgSetPriority`.
* **BG0**: "HURRY UP" text, end-of-stage results.
* **BG1**: Tiles, walls, teleporters and turrets.
* **BG2**: Bullets, particles, lasers and polygonal effects.
* **BG3**: Bitmap backgrounds.

The HUD and all its values will be rendered on the bottom screen, likely with a custom image.

**TODO**: What VRAM bank arrangement shall be used?

## Audio

**TODO**: Perhaps have [Maxmod](https://maxmod.org/) handle the audio?

## Gameplay

The gameplay will be preserved as well as possible, with player controls, scoring, boss behavior etc. kept close to the original. Bugs and code oddities will be removed.

Due to the much smaller screen of the DS, as well as it's narrower aspect ratio, the playfield must be shrunken from the original. This has some consequences:
* Boss behavior will have to be altered accordingly.
* Stages will have to be altered, since the screen is now 16 tiles wide instead of 20; on a case by case basis, each stage will either have certain columns removed, or be squished, or be cropped.

As for the controls, Left, Right, A, B and Start will function during gameplay exactly like Left, Right, X, Z and Esc did in the original game, except that Left and Right will be assumed to never be inputted simultaneously. The X button will be added as a new way to trigger bombs.

## Menus

### Main menu

The main menu will be navigable using both button controls and touch controls. An option to access the high score screen will be added.

The top screen will show the game logo, and the bottom will show the options and the ZUN copyright notice.

## Results screen

Results will be shown on both the top and bottom screen.

#!/usr/bin/env python3
import argparse
import struct
import sys
from pathlib import Path

import halve_image

HEADER_SIZE = 6
PALETTE_COLORS = 16
PALETTE_SIZE = PALETTE_COLORS * 3

PLANE_ROW_BYTES = 4
PLANE_SIZE = 128
IMAGE_DATA_SIZE = 1 + (4 * PLANE_SIZE)

def decode_palette(pal_bytes: bytes) -> list[int]:
    colors = []
    for i in range(PALETTE_COLORS):
        r, g, b = pal_bytes[i * 3 : i * 3 + 3]
        # r, g and b range from 0 to 15.
        ds_r = (r * 0x11 >> 3)
        ds_g = (g * 0x11 >> 3)
        ds_b = (b * 0x11 >> 3)
        ds_color = (ds_b << 10) | (ds_g << 5) | (ds_r << 0)
        colors.append(ds_color)
    return [colors[15]] + colors[:15]

def decode_chunk(chunk: bytes) -> list[list[int]]:
    plane_bytes = chunk[1:]
    planes = {
        "B": plane_bytes[0 * PLANE_SIZE : 1 * PLANE_SIZE],
        "R": plane_bytes[1 * PLANE_SIZE : 2 * PLANE_SIZE],
        "G": plane_bytes[2 * PLANE_SIZE : 3 * PLANE_SIZE],
        "E": plane_bytes[3 * PLANE_SIZE : 4 * PLANE_SIZE],
    }

    image = []
    for y in range(32):
        row_off = y * PLANE_ROW_BYTES
        b_row = planes["B"][row_off : row_off + PLANE_ROW_BYTES]
        r_row = planes["R"][row_off : row_off + PLANE_ROW_BYTES]
        g_row = planes["G"][row_off : row_off + PLANE_ROW_BYTES]
        e_row = planes["E"][row_off : row_off + PLANE_ROW_BYTES]
        image_row = [];
        for x in range(32):
            byte_idx = x // 8
            bit_idx = 7 - (x % 8)  # MSB-first
            b = (b_row[byte_idx] >> bit_idx) & 1
            r = (r_row[byte_idx] >> bit_idx) & 1
            g = (g_row[byte_idx] >> bit_idx) & 1
            e = (e_row[byte_idx] >> bit_idx) & 1
            index = (e << 3) | (g << 2) | (r << 1) | b
            index = (index + 1) % 16
            image_row.append(index)
        image.append(image_row)
    return image

def pack_frame_4bpp(pixels: list[list[int]]) -> list[int]:
    height = len(pixels)
    width = len(pixels[0]) if height else 0
    if width == 0 or height == 0:
        raise ValueError("empty frame")
    if width % 8 or height % 8:
        raise ValueError(
            f"sprite dimensions must be multiples of 8 for 4bpp tiles; got {width}x{height}"
        )

    out: list[int] = []
    for tile_y in range(0, height, 8):
        for tile_x in range(0, width, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    lo = pixels[tile_y + y][tile_x + x] & 0x0F
                    hi = pixels[tile_y + y][tile_x + x + 1] & 0x0F
                    out.append(lo | (hi << 4))
    words = [
        int.from_bytes(out[i : i + 4], byteorder="little")
        for i in range(0, len(out), 4)
    ]
    return words

def decode_ptn(data: bytes):
    magic, _, image_count = struct.unpack_from("<4sbb", data, 0)
    if magic != b"HPTN":
        raise ValueError(f"bad magic {magic!r}, expected HPTN")

    pal_start = HEADER_SIZE
    pal_end = pal_start + PALETTE_SIZE
    palette = decode_palette(data[pal_start:pal_end])

    images = []
    offset = pal_end
    for i in range(image_count):
        chunk = data[offset : offset + IMAGE_DATA_SIZE]
        if len(chunk) < IMAGE_DATA_SIZE:
            raise ValueError(
                f"file truncated: image {i}/{image_count} needs "
                f"{IMAGE_DATA_SIZE} bytes at offset {offset}, only "
                f"{len(chunk)} available"
            )
        images.append(decode_chunk(chunk))
        offset += IMAGE_DATA_SIZE
    return palette, images

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ptn_file", type=Path, help="input .PTN file")
    parser.add_argument("outdir", type=Path, help="directory for generated .h file")
    parser.add_argument("name", type=str, help="name of the generated sprite")
    parser.add_argument("--halve", type=str, default="", help="method to halve the size of sprites", required=False)
    parser.add_argument("-s", "--sprite", nargs='+', type=int, default=[], help="sprite indices", required=False)
    parser.add_argument("-q", "--quarter", action=argparse.BooleanOptionalAction, help="whether frames should be split into quarters")
    args = parser.parse_args()

    if args.ptn_file.suffix.lower() != ".ptn":
        parser.error(f"input does not have a .PTN extension: {args.ptn_file}")
    if not args.ptn_file.is_file():
        parser.error(f"input file does not exist: {args.ptn_file}")

    if args.halve and args.halve not in halve_image.HALF_METHODS_LIST:
        parser.error(f"invalid halving method {args.halve}")

    try:
        data = args.ptn_file.read_bytes()
        palette, images = decode_ptn(data)
        if args.sprite:
            images = [images[i] for i in args.sprite]
        # quartering
        if args.quarter:
            new_images = []
            for image in images:
                new_images.append([row[:16] for row in image[:16]])
                new_images.append([row[16:] for row in image[:16]])
                new_images.append([row[:16] for row in image[16:]])
                new_images.append([row[16:] for row in image[16:]])
            images = new_images
        # halving
        if args.halve:
            images = [halve_image.shrink_image(image, args.halve) for image in images]
        # packing
        images = [pack_frame_4bpp(image) for image in images]
        args.outdir.mkdir(parents=True, exist_ok=True)
        output_path = args.outdir / f"{args.name}.h"
        write_header(output_path, args.name, images, palette)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0

def write_header(path: Path, name: str, frames: list[list[int]], palette: list[int]) -> None:
    lines = [f"// {len(frames)} frames",
        f"const unsigned int {name}_tiles[{len(frames) * len(frames[0])}] =", "{"]
    for frame in frames:
        for j in range(0, len(frame), 8):
            chunk = frame[j : j + 8]
            suffix = ","
            lines.append("\t" + ",".join(f"0x{value:08X}" for value in chunk) + suffix)
        lines.append("")
    lines.append("};\n")
    
    lines.append(f"const unsigned short {name}_palette[{len(palette)}] __attribute__((aligned(4))) = ")
    lines.append("{")
    lines.append("\t" + ", ".join(f"0x{value:04X}" for value in palette[:8]) + ",")
    lines.append("\t" + ", ".join(f"0x{value:04X}" for value in palette[8:]))
    lines.append("};")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")

if __name__ == "__main__":
    raise SystemExit(main())
import numpy as np

HALF_METHODS_LIST = ["topleft", "topleft2", "stagger", "dither"]

def halve_topleft(image: list[list[int]]) -> list[list[int]]:
    new_image = []
    y_size = len(image)
    x_size = len(image[0])
    for y in range(0, y_size, 2):
        upper_row = []
        for x in range(0, x_size, 2):
            upper_row.append(image[y  ][x  ])
        new_image.append(upper_row)
    return new_image

def halve_topleft2(image: list[list[int]]) -> list[list[int]]:
    new_image = []
    y_size = len(image)
    x_size = len(image[0])
    for y in range(0, y_size, 4):
        upper_row = []
        lower_row = []
        for x in range(0, x_size, 4):
            upper_row.append(image[y  ][x  ])
            upper_row.append(image[y  ][x+1])
            lower_row.append(image[y+1][x  ])
            lower_row.append(image[y+1][x+1])
        new_image.append(upper_row)
        new_image.append(lower_row)
    return new_image

def halve_stagger(image: list[list[int]]) -> list[list[int]]:
    new_image = []
    y_size = len(image)
    x_size = len(image[0])
    for y in range(0, y_size, 4):
        upper_row = []
        lower_row = []
        for x in range(0, x_size, 4):
            upper_row.append(image[y  ][x  ])
            upper_row.append(image[y+1][x+2])
            lower_row.append(image[y+2][x+1])
            lower_row.append(image[y+3][x+3])
        new_image.append(upper_row)
        new_image.append(lower_row)
    return new_image

def halve_dither(image: list[list[int]]) -> list[list[int]]:
    y_size = len(image)
    x_size = len(image[0])
    dither_template = np.zeros((y_size // 2, x_size // 2, 16))
    for y in range(0, y_size):
        for x in range(0, x_size):
            dither_template[y // 2, x // 2, image[y][x]] += 0.25
    new_image = []
    for y in range(0, y_size // 2):
        new_row = []
        for x in range(0, x_size // 2):
            chosen_index = np.argmax(dither_template[y,x])
            new_row.append(chosen_index)
            diff = np.identity(16)[chosen_index] - dither_template[y,x]
            if x + 1 < x_size / 2:
                dither_template[y,x+1] -= diff * (7/16)
            if y + 1 < y_size / 2:
                dither_template[y+1,x] -= diff * (5/16)
                if x + 1 < x_size / 2:
                    dither_template[y+1,x+1] -= diff * (1/16)
                if x > 0:
                    dither_template[y+1,x-1] -= diff * (3/16)
        new_image.append(new_row)
    return new_image

def shrink_image(image: list[list[int]], method: str) -> list[list[int]]:
    if not method:
        return image
    if method == "topleft":
        return halve_topleft(image)
    if method == "topleft2":
        return halve_topleft2(image)
    if method == "stagger":
        return halve_stagger(image)
    if method == "dither":
        return halve_dither(image)
    raise ValueError(f"invalid halving method {method}")
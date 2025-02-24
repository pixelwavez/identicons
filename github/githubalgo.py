from colorsys import hsv_to_rgb
from hashlib import sha1
from random import uniform
from typing import List, Tuple
from PIL import Image, ImageDraw
from argparse import ArgumentParser

## COLOR GENERATORS


# (r, g, b) from a byte
def get_color(hexdigest: str) -> Tuple[int, int, int]:
    r = int(hexdigest[6:8], 16)
    g = int(hexdigest[8:10], 16)
    b = int(hexdigest[10:12], 16)
    return (r, g, b)


# for multicolor use
def get_pixel_color(hexdigest: str, x: int, y: int) -> Tuple[int, int, int]:
    r = int(hexdigest[(x * 2) % len(hexdigest)], 16) * 16
    g = int(hexdigest[(y * 2 + 1) % len(hexdigest)], 16) * 16
    b = int(hexdigest[(x + y) % len(hexdigest)], 16) * 16
    return (r % 256, g % 256, b % 256)


# base color with hue mutations
def get_hue_mutation_color(hexdigest: str, x: int, y: int) -> Tuple[int, int, int]:
    base_hue = int(hexdigest[:2], 16) / 255.0

    # vary the hue slightly within a range (-0.1 to +0.1)
    hue_variation = base_hue + uniform(-0.1, 0.1)
    hue_variation = max(0.0, min(1.0, hue_variation))

    saturation = 0.8
    value = 0.9

    r, g, b = hsv_to_rgb(hue_variation, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))


## IDENTICON GENERATORS


# generate a 5x5 array of bits — only uses 5 hex digits
def generate_pattern_simple(hexdigest: str) -> List[List[int]]:
    bit_array = []

    # only need 5 hex digits — one for each row
    for i in range(5):
        row_int_val = int(hexdigest[i], 16)
        row_array = [
            (row_int_val >> j) & 1 for j in range(3)
        ]  # only need 3 bits and then mirror
        row_array += row_array[:2][::-1]  # mirror
        bit_array.append(row_array)

    return bit_array


# uses 4 hex values per row
def generate_pattern_4hex_row(hexdigest: str) -> List[List[int]]:
    bit_array = []

    for i in range(5):
        row_int_val = int(
            hexdigest[i * 2 : i * 2 + 4], 16
        )  # take 4 hex digits at a time
        row_array = [
            (row_int_val >> j) & 1 for j in range(6)
        ]  # extract 6 bits for more complexity
        row_array += row_array[:3][::-1]  # mirror
        bit_array.append(row_array)

    return bit_array


def hash_user_id(user_id: str) -> str:
    return sha1(user_id.encode()).hexdigest()


def render(
    user_id: str, identicon_generator_func, multicolor: bool, color_generator_func
) -> None:
    pixel_size, image_size = 50, 250

    hexdigest = hash_user_id(user_id)
    bit_array = identicon_generator_func(hexdigest)
    color = COLOR_PATTERN_GENERATOR_MAP["single"](hexdigest)

    img = Image.new("RGB", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(bit_array):
        for p, pixel in enumerate(row):
            if pixel:
                tl_x, tl_y = p * pixel_size, r * pixel_size
                br_x, br_y = tl_x + pixel_size, tl_y + pixel_size
                if multicolor:
                    draw.rectangle(
                        xy=[tl_x, tl_y, br_x, br_y],
                        fill=color_generator_func(hexdigest=hexdigest, x=p, y=r),
                    )
                else:
                    draw.rectangle(xy=[tl_x, tl_y, br_x, br_y], fill=color)

    img.show()


IDENTICON_PATTERN_GENERATOR_MAP = {
    "simple": generate_pattern_simple,
    "4hex": generate_pattern_4hex_row,
}

COLOR_PATTERN_GENERATOR_MAP = {
    "single": get_color,
    "multi": get_pixel_color,
    "hues":get_hue_mutation_color
}


def github_identicon(
    user_id: str,
    identicon_pattern_generator: str = "simple",
    color_pattern_generator: str = "single",
) -> None:
    if identicon_pattern_generator not in IDENTICON_PATTERN_GENERATOR_MAP:
        print(f"Identicon pattern '{identicon_pattern_generator}' not found")
        return

    if color_pattern_generator not in COLOR_PATTERN_GENERATOR_MAP:
        print(f"Color pattern '{color_pattern_generator}' not found")
        return

    render(
        user_id,
        IDENTICON_PATTERN_GENERATOR_MAP[identicon_pattern_generator],
        color_pattern_generator != "single",
        COLOR_PATTERN_GENERATOR_MAP[color_pattern_generator],
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="GitHub Identicon Argparser.")
    parser.add_argument(
        "-u", "--user", "--id", "--userid", required=True, type=str, help="User ID"
    )
    parser.add_argument(
        "-p", "--pattern", type=str, help="Specify identicon pattern generator"
    )

    parser.add_argument(
        "-c", "--colorpattern", type=str, help="Specify color pattern generator"
    )

    args = parser.parse_args()

    user_id = args.user

    identicon_pattern_generator = "simple"
    if args.pattern:
        identicon_pattern_generator = args.pattern

    color_pattern_generator = "single"
    if args.colorpattern:
        color_pattern_generator = args.colorpattern

    github_identicon(user_id, identicon_pattern_generator, color_pattern_generator)

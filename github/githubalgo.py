from hashlib import sha1
from typing import List, Tuple
from PIL import Image, ImageDraw
from argparse import ArgumentParser


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


def render(user_id: str, pattern_generator_func, multicolor: bool = False) -> None:
    pixel_size, image_size = 50, 250

    hexdigest = hash_user_id(user_id)
    bit_array = pattern_generator_func(hexdigest)
    color = get_color(hexdigest)

    img = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(bit_array):
        for p, pixel in enumerate(row):
            if pixel:
                tl_x, tl_y = p * pixel_size, r * pixel_size
                br_x, br_y = tl_x + pixel_size, tl_y + pixel_size
                if multicolor:
                    draw.rectangle(
                        xy=[tl_x, tl_y, br_x, br_y],
                        fill=get_pixel_color(hexdigest=hexdigest, x=p, y=r),
                    )
                else:
                    draw.rectangle(xy=[tl_x, tl_y, br_x, br_y], fill=color)

    img.show()


PATTERN_GENERATOR_MAP = {
    "simple": generate_pattern_simple,
    "4hex": generate_pattern_4hex_row,
}


def github_identicon(
    user_id: str, multicolor: bool = False, pattern_generator: str = "simple"
) -> None:
    if not user_id:
        print("UserID not provided")
        return

    if pattern_generator not in PATTERN_GENERATOR_MAP:
        print(f"Pattern {pattern_generator} not found")
        return

    render(
        user_id=user_id,
        pattern_generator_func=PATTERN_GENERATOR_MAP[pattern_generator],
        multicolor=multicolor,
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="GitHub Identicon Argparser.")
    parser.add_argument(
        "-u", "--user", "--id", "--userid", required=True, type=str, help="User ID"
    )
    parser.add_argument("-p", "--pattern", type=str, help="Specify pattern generator")
    parser.add_argument(
        "-m", "--multicolor", action="store_true", help="Specify pattern generator"
    )

    args = parser.parse_args()

    user_id = args.user

    pattern_generator = "simple"
    if args.pattern:
        pattern_generator = args.pattern

    multicolor = False
    if args.multicolor:
        multicolor = True

    github_identicon(
        user_id=user_id, pattern_generator=pattern_generator, multicolor=multicolor
    )

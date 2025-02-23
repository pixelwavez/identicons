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


# generate a 5x5 array of bits
def generate_bit_array(hexdigest: str) -> List[List[int]]:
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


def hash_user_id(user_id: str) -> str:
    return sha1(user_id.encode()).hexdigest()


def render(user_id: str, pixel_size: int = 50, image_size: int = 250) -> None:
    hexdigest = hash_user_id(user_id)
    bit_array = generate_bit_array(hexdigest)
    color = get_color(hexdigest)

    img = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(bit_array):
        for p, pixel in enumerate(row):
            if pixel:
                tl_x, tl_y = p * pixel_size, r * pixel_size
                br_x, br_y = tl_x + pixel_size, tl_y + pixel_size
                draw.rectangle(xy=[tl_x, tl_y, br_x, br_y], fill=color)

    img.show()


def github_identicon(user_id: str) -> None:
    if not user_id:
        print("UserID not provided")
    render(user_id)


if __name__ == "__main__":
    parser = ArgumentParser(description="GitHub Identicon Argparser.")
    parser.add_argument("-u", "--user", "--id", "--userid", type=str, help="User ID")

    args = parser.parse_args()

    user_id = None
    if args.user:
        user_id = args.user
    github_identicon(user_id)

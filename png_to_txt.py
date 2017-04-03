#!/usr/bin/env python3
import argparse
import os
from PIL import Image


def print_img(img):
    width, height = img.size
    for y in range(height):
        for x in range(width):
            print("█" if is_black(img.getpixel((x, y))) else " ", end="")  # full block is U+2588
        print()


def get_rows(img, full=False):
    width, height = img.size
    rows, counter = [], 0
    for y in range(height):
        row = []
        for x in range(width):
            value = is_black(img.getpixel((x, y)))
            if value:
                counter += 1
            if not value or x == width - 1:
                if counter != 0:
                    row.append(counter)
                counter = 0
        rows.append(row)
    return rows if full else [sum(r) for r in rows]


def get_cols(img, full=False):
    width, height = img.size
    cols, counter = [], 0
    for x in range(width):
        col = []
        for y in range(height):
            value = is_black(img.getpixel((x, y)))
            if value:
                counter += 1
            if not value or y == height - 1:
                if counter != 0:
                    col.append(counter)
                counter = 0
        cols.append(col)
    return cols if full else [sum(c) for c in cols]


def is_black(pix):
    return pix < 128


if __name__ == '__main__':
    # argparse definitions
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to the image')
    parser.add_argument('-p', action='store_true', help='Print the image in the shell')
    parser.add_argument('-f', action='store_true', help='Output full description of rows and cols')

    # argparse parsing
    args = parser.parse_args()
    img_path = args.path
    txt_path = os.path.splitext(img_path)[0] + '.txt'
    img = Image.open(img_path).convert('1', dither=False)  # open and convert to black OR white
    full = args.f
    if args.p:
        print_img(img)

    # write path
    with open(txt_path, 'wt') as f:
        d = ", ".join(str(r) for r in get_rows(img, full)) + '\n'
        d += ", ".join(str(c) for c in get_cols(img, full))
        f.write(d)
        print(d)

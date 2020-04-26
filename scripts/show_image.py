#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path

import logging
logging.basicConfig(level = logging.DEBUG)
from rpi_waveshare_pyepd import display_variants, epd_calibrate, epd_show

def rotate(image, orientation):
    if orientation == "p":
        image = image.transpose(Image.ROTATE_90)
    elif orientation == "lf":
        image = image.transpose(Image.ROTATE_180)
    elif orientation == "pf":
        image = image.transpose(Image.ROTATE_270)

    return image

def process_image(image, display_colours):

    buffer = np.array(image)
    r_arr, g_arr, b_arr = buffer[:,:,0], buffer[:,:,1], buffer[:,:,2]
    if display_colours == "bwr":
        buffer[np.logical_and(r_arr > 245, g_arr > 245)] = [255,255,255] #white
        buffer[np.logical_and(r_arr > 245, g_arr < 245)] = [255,0,0] #red
        buffer[np.logical_and(r_arr != 255, r_arr == g_arr )] = [0,0,0] #black

    if display_colours == "bw":
        buffer[np.logical_and(r_arr > 245, g_arr > 245)] = [255,255,255] #white
        buffer[g_arr < 255] = [0,0,0] #black

    return  Image.fromarray(buffer)

if __name__ == '__main__':
    possible_diplays = ", ".join(["'{}' : {}".format(key, display_variants[key]["name"]) for key in display_variants.keys()])
    parser = argparse.ArgumentParser(description='print image on eink.')
    parser.add_argument('--type', type=str, default='epd7in5',
                        help=possible_diplays)
    parser.add_argument('source_file', type=Path,
                        help='current screenshot')
    parser.add_argument('--orientation', type=str, choices=["p", "pf", "l", "lf"],
                        default='p', help= ('orientation of source_image: p = portrait, ' +
                        'pf = portrait flipped, l = landscape, '+
                        'lf = landscape flipped'))
    args = parser.parse_args()
    image = Image.open(str(args.source_file)).convert("RGB")
    image = rotate(image, args.orientation)

    epd_calibrate(args.type)
    epd_show(image, args.type)

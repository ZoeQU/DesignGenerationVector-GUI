# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import math
from random import randint as ri
from random import uniform as rf
import random
import lxml.etree as ET
from xml.dom import minidom
import time
import argparse
import sys
from operator import itemgetter
import itertools
from collections import defaultdict, Counter
import numpy as np
import cv2  # 3.4.2
import imutils
import os
import cairosvg
from matplotlib import pyplot as plt

from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

from utils.colorize_functions import (rgb_to_hex, hex_random, generate_color_palette,
                                      show_color_blocks) 
from .generate_functions import (generate_new_svg, striperowgroup, generate_random_width, 
                                draw_sequence, cal_loc, stripe_pathes)


class Stripe():
    def __init__(self) -> None:
        self.savenames = []
        self.color_palette_cache = None
        self.color_block_path = None

    def _generate_stripe_pattern(self, img, num, index):
        width = 200
        height = 200
        stripe_num = ri(2,10)
        if stripe_num < num:
            stripe_num = num

        patternwidth = 4 * width
        patternheight = 4 * height

        # color, sorted_color, labels = generate_color_palette(img, num) 
        # color_block_path = processPath + 'stripe_' + str(num) + '_color_blocks.png'
        # show_color_blocks(sorted_color, color_block_path)

        # Generate color palette (only for the first call)
        if index == 0:
            self.color_block_path = processPath + 'color_palette.png'
            color, sorted_color, pantone_codes, labels = generate_color_palette(img, num) 
            show_color_blocks(sorted_color, self.color_block_path, pantone_codes)

            self.color_palette_cache = (color, sorted_color)
        else:
            if self.color_palette_cache is None:
                raise ValueError("Color palette cache is empty. Ensure index=0 is called first.")
            color, sorted_color = self.color_palette_cache

        viewBox = '0 0 ' + str(patternwidth) + ' ' + str(patternheight)

        widths = generate_random_width(width, stripe_num)
        pathes = stripe_pathes(height, widths, color, num)

        stripe_header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
                        'width="' + str(patternwidth) + '" height="' + str(patternheight) + '" viewBox="' + str(viewBox) + '"' + '\n' \
                        'preserveAspectRatio = "xMidYMid meet" >'

        row = striperowgroup(pathes, width)

        pathes = []
        for r in range(4):
            pathes.append('<g id="row' + str(r) + '" ' + 'transform=' +
                        '"translate(' + str(int(0)) +
                        ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
            for k in row:
                pathes.append(k + '\n')
            pathes.append('</g>' + '\n')


        savename = savePath + 'stripe_' + str(index) + '.svg' 
        savename_ = savePath + 'stripe_' + str(index) + '.png'  
        generate_new_svg(savename, stripe_header, pathes, new_bk_rect='')
        cairosvg.svg2png(url=savename, write_to=savename_)

        return savename, self.color_block_path

    def generate_stripe_pattern(self, img, num):
        for i in range(6):
            savename, self.color_block_path = self._generate_stripe_pattern(img, num, i)
            self.savenames.append(savename)

        return self.savenames, self.color_block_path

if __name__ == "__main__":
    img_path = "/home/zoe/ResearchProjects/DesignGenerationVector/data/color_ref/color_ref_0.jpg"
    img = cv2.imread(img_path)
    stripe = Stripe()
    color_block_path = stripe.generate_stripe_pattern(img, num=3)
    print("biu~biu~biu~")


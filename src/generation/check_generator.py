# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import math
from random import randint as ri
from random import uniform as rf
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


savenames = []

def _generate_check_pattern(img, num, index):
    width = 200
    height = 200
    patternwidth = 4 * width
    patternheight = 4 * height
    num_w = ri(2,10)

    if num_w < num:
        num_w = num
    num_h = ri(2,10)
    if num_h < num:
        num_h = num
    viewBox = '0 0 ' + str(patternwidth) + ' ' + str(patternheight)

    # color_block_path = processPath + 'check_' + str(num) + '_color_blocks.png'
    # color, sorted_color, labels = generate_color_palette(img, num) 
    # show_color_blocks(sorted_color, color_block_path)

    # Generate color palette (only for the first call)
    if index == 0:
        color_block_path = processPath + 'color_palette.png'
        color, sorted_color, pantone_codes, _ = generate_color_palette(img, num) 
        show_color_blocks(sorted_color, color_block_path, pantone_codes)
    else:
        color_block_path = None

    # vertical stripes 
    widths = generate_random_width(width, num_w)
    pathes_w = stripe_pathes(height, widths, color, num)

    # horizontal stripes
    num_ = ri(2, num)
    heights = generate_random_width(width, num_h)
    pathes_h = stripe_pathes(height, heights, color, num_)

    # generate check
    rotate_param = (90, int(width/2), int(height / 2))
    transform_ = ['<g transform = "rotate' + str(rotate_param) + '" fill-opacity="0.7">']
    pathes = pathes_w + transform_ + pathes_h + ['</g>']
    
    # layout-row
    row = striperowgroup(pathes, width)
    
    # generate check pattern
    pathes = []
    for r in range(4):
        pathes.append('<g id="row' + str(r) + '" ' + 'transform=' +
                      '"translate(' + str(int(0)) +
                      ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
        for k in row:
            pathes.append(k + '\n')
        pathes.append('</g>' + '\n')

    check_header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
                   'width="' + str(patternwidth) + '" height="' + str(patternheight) + '" viewBox="' + str(viewBox) + '"' + '\n' \
                   'preserveAspectRatio = "xMidYMid meet" >'

    savename = savePath + 'check_' + str(index) + '.svg'
    savename_ = savePath + 'check_' + str(index) + '.png'
    generate_new_svg(savename, check_header, pathes, new_bk_rect='')
    cairosvg.svg2png(url=savename, write_to=savename_)

    return savename, color_block_path
    

def generate_check_pattern(img, num):
    for i in range(6):
        savename, color_block_path = _generate_check_pattern(img, num, i)
        savenames.append(savename)

    return savenames, color_block_path

if __name__ == "__main__":
    img_path = "/home/zoe/ResearchProjects/DesignGenerationVector/data/color_ref/color_ref_0.jpg"
    img = cv2.imread(img_path)
    savename, color_block_path = generate_check_pattern(img, num=9)
    print("biu~biu~biu~")


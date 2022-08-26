# -*- coding:utf-8 -*-
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

from utils.func_random import random_bk_rect, random_process_path, hex_random
from utils.func_read import read_svg
from utils.func_generate import generate_new_svg
from utils.stripe_generate import stripe_pathes, random_width
from utils.design_generation import colgroup, rowgroup


def check_generate(width, height, num, color, na, a, outputCheck):
    patternwidth = 4 * width
    patternheight = 4 * height

    viewBox = '0 0 ' + str(patternwidth) + ' ' + str(patternheight)

    # num = ri(3, 6)
    # 生成竖条纹
    widths = random_width(width, num)
    pathes_w = stripe_pathes(height, widths, color, num)
    # 生成横条纹
    heights = random_width(height, num)
    pathes_h = stripe_pathes(height, heights, color, num)
    # 组合check
    rotate_param = (90, int(width/2), int(height / 2))
    transform_ = ['<g transform = "rotate' + str(rotate_param) + '" fill-opacity="0.7">']
    pathes = pathes_w + transform_ + pathes_h + ['</g>']
    # 组合row
    row = rowgroup(pathes, width)
    # 组合pattern
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

    savename = outputCheck + 'check_new_' + str(na) + '_' + str(a) + '.svg'  # need to modify
    generate_new_svg(savename, check_header, pathes, new_bk_rect='')


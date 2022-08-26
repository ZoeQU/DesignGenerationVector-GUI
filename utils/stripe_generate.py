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
from utils.ColorPalettePredict import ColorPalettePredict
from utils.func_read import Hex2Rgb, RGB_to_Hex
from utils.design_generation import colgroup, rowgroup


# def _random_width(width):
#     a1 = ri(10, int(width / 3))
#     a2 = ri(0, width - a1)
#     a3 = ri(0, width - a1 - a2)
#     a4 = ri(0, width - a1 - a2 - a3)
#     a5 = width - a1 - a2 - a3 - a4
#     return [a1, a2, a3, a4, a5]


def cal_left(width, a):
    left = width - sum(a)
    return left


def random_width(width, n):
    a0 = ri(10, int(width / n))
    a = [a0]
    for i in range(n - 2):
        left = cal_left(width, a)
        a1 = ri(0, left)
        a.append(a1)
    a_ = width - sum(a)
    a.append(a_)
    return a


def cal_loc(ls):
    b = [0]
    for i in range(len(ls) - 1):
        _b = sum(ls[:i + 1])
        b.append(_b)
    return b


def stripe_pathes(height, width_s, color, num):
    pathes = []
    loc_x = cal_loc(width_s)
    for i in range(len(width_s)):
        """1. random color"""
        # rect_color = hex_random()
        """2. from ref color image"""
        rect_color = RGB_to_Hex(color[i][2])

        rect_path = '<rect x="' + str(loc_x[i]) + '" y="0" width="' + \
                    str(width_s[i]) + '" height="' + str(height) + \
                    '" fill="' + str(rect_color) + '"/>'

        pathes.append(rect_path)
    return pathes


def stripe_generate(width, height, num, color, na, a, outputStripe):
    patternwidth = 4 * width
    patternheight = 4 * height

    viewBox = '0 0 ' + str(patternwidth) + ' ' + str(patternheight)
    widths = random_width(width, num)
    pathes = stripe_pathes(height, widths, color, num)

    stripe_header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
                    'width="' + str(patternwidth) + '" height="' + str(patternheight) + '" viewBox="' + str(viewBox) + '"' + '\n' \
                    'preserveAspectRatio = "xMidYMid meet" >'

    row = rowgroup(pathes, width)

    pathes = []
    for r in range(4):
        pathes.append('<g id="row' + str(r) + '" ' + 'transform=' +
                      '"translate(' + str(int(0)) +
                      ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
        for k in row:
            pathes.append(k + '\n')
        pathes.append('</g>' + '\n')

    savename = outputStripe + 'stripe_new_' + str(na) + '_' + str(a) + '.svg'  # need to modify
    generate_new_svg(savename, stripe_header, pathes, new_bk_rect='')
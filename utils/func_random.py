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


def hex_random():
    """生成一个随机的hex值"""
    # color: int
    color1 = ri(0, 255)
    color2 = ri(0, 255)
    color3 = ri(0, 255)
    color1 = hex(color1)
    color2 = hex(color2)
    color3 = hex(color3)
    ans = "#" + color1[2:] + color2[2:] + color3[2:]
    return ans


def random_bk_rect(rect_color, height, width):
    bk_color = hex_random()
    bk_rect = '<rect width="' + str(width) + '" height="' + str(height) + '" fill="' + str(bk_color) + '"/>'
    return bk_rect


def random_process_path(path, height, width):
    """transformation"""
    fillcolor = hex_random()
    translate_param = (ri(0, int(width/10)), ri(0, int(height/10)))
    rotate_param = (ri(0, 90), int(width/2), int(height / 2))
    skewX_param = (ri(0, 20))
    skewY_param = (ri(0, 20))
    scale_param = (round(rf(0.8, 1), 2), round(rf(0.8, 1), 2))
    # 'trasnlate' + str(translate_param) +
    path_new = '<path d="' + str(path) + '"' + ' transform="' + 'scale' + str(scale_param) + 'rotate' + str(rotate_param) + 'skewX(' + str(skewX_param) + ')" stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
    return path_new





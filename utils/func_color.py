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


def temp_svg(path_i, width, height, viewBox, processPath):
    """
    根据输入的svg path信息生成一个svg文件
    :param path_i: svg路径信息
    :param width: svg文件head信息
    :param height: svg文件head信息
    :param viewBox: svg文件head信息
    :param processPath: 存放地址文件夹
    :return: svg文件
    """
    header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
             'width="' + str(width) + '" height="' + str(height) + \
             '" viewBox="' + str(viewBox) + '"' + '\n' \
            'preserveAspectRatio = "xMidYMid meet" >'
    tempname = processPath + 'temp.svg'
    with open(tempname, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write(path_i + '\n')
        svg.write("</svg>")
    svg.close()
    return tempname
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
from PIL import Image
from matplotlib import pyplot as plt


def temp_svg(path_i, header, temp_folder, width, height):
    """
    根据输入的svg path信息生成一个svg文件
    """
    tempname = temp_folder + 'temp.svg'
    bk = '<rect width="' + str(width) + '" height="' + str(height) + '" fill="' + '#ffffff' + '"/>'
    with open(tempname, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write(bk + '\n')
        svg.write(path_i + '\n')
        svg.write("</svg>")
    svg.close()
    return tempname


def Hex2Rgb(value):
    """将16进制Hex 转化为 [R,G,B]"""
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def RGB_to_Hex(rgb):
    """将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示"""
    # RGB = rgb.split(',')            # 将RGB格式划分开来 str format
    color = '#'
    for i in rgb:
        if np.isnan(i):
            i = 255
        else:
            num = int(i)
            color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


def cal_area(tempname, width, height, color):
    """
   计算背景颜色所占的面积比
   :param temppng: 图片
   :return:
   """
    # # img method 2 ##
    temppng = cv2.imread(tempname, cv2.IMREAD_COLOR)

    if len(temppng.shape) == 2:
        area = np.sum(temppng == 0)
        arearate = area / (width * height)
    else:
        r, g, b = cv2.split(temppng)
        im = r + g + b
        area = np.sum(im == 0)
        arearate = area / (width * height)
    return arearate


def cal_svg_info(path_info, header, temp_folder, width, height):
    color_info = []
    colors = []
    for j in path_info:
        pp = j[0]
        fillcc = '#000000'
        path_i = '<path d="' + pp + '" transform="translate(0.000000,' + str(height) + ')'\
                 ' scale(0.100000,-0.100000)" stroke="none" '\
                 'fill="' + fillcc + '"/>\n'
        tempsvg = temp_svg(path_i, header, temp_folder, width, height)
        temppng = temp_folder + 'temp.png'
        cairosvg.svg2png(url=tempsvg, write_to=temppng)

        color = Hex2Rgb(j[1])
        colors.append(j[1])

        arearate = cal_area(temppng, width, height, color)
        os.remove(tempsvg)  # 删除临时 bk.svg 文件
        os.remove(temppng)  # 删除临时 bk.png 文件
        color_info.append([color, arearate])

    colors_ = set(colors)
    color_info_ = []
    for i in colors_:
        cc = Hex2Rgb(i)
        color_amount = 0
        for j in color_info:
            if j[0] == cc:
                color_amount += j[1]
        color_info_.append([i, color_amount])

    return color_info_


def read_svg(svg_name, temp_folder):
    """
    minidom.parse 和 ET.parse(open(svg_name, 'r'))
    两种不同的读取svg文件的方法，
    侧重点不同，因此用两种方式读取
    :param svg_name:
    :return:
    """
    tree = ET.parse(open(svg_name, 'r'))
    root = tree.getroot()
    height = root.attrib['height']
    width = root.attrib['width']
    height = 1 * int(height.split('.')[0])
    width = 1 * int(width.split('.')[0])
    viewBox = '0 0 ' + str(width) + ' ' + str(height)
    header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n'\
             'width="' + str(width) + '" height="' + str(height) + \
             '" viewBox="' + str(viewBox) + '"' + '\n' \
             'preserveAspectRatio = "xMidYMid meet" >'

    doc = minidom.parse(svg_name)
    bk_hex = [rect.getAttribute('fill') for rect
              in doc.getElementsByTagName('rect')]

    pathes = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

    path_info = [[path.getAttribute('d'), path.getAttribute('fill')]
                 for path in doc.getElementsByTagName('path')]

    """calculate path area"""
    color_info_ = cal_svg_info(path_info, header, temp_folder, width, height)

    bk_area = 1
    for j in color_info_:
        bk_area -= j[1]
    color_info_.append([bk_hex[0], bk_area])
    color_info_ = sorted(color_info_, key=lambda k: k[1])

    doc.unlink()

    return color_info_, header, height, width, bk_hex, pathes



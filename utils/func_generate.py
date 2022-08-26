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
    tempname = processPath + 'temp.svg'

    header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
             'width="' + str(width) + '" height="' + str(height) + \
             '" viewBox="' + str(viewBox) + '"' + '\n' \
             'preserveAspectRatio = "xMidYMid meet" >'

    with open(tempname, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write(path_i + '\n')
        svg.write("</svg>")
    svg.close()
    return tempname


def generate_new_svg(savename, header, pathes_new, new_bk_rect):
    """
    生成新的svg, 并添加了 bk path
    :param savename: 生成的svg名字
    :param header: 添加header信息
    :param pathes_new: 列表，每个元素代表新的path
    :param new_bk_rect: 新的bk path
    :return:
    """
    with open(savename, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write('<metadata>\n'
                  'Created by ZoeQu, written in 2022\n'
                  '</metadata>\n')
        svg.write(new_bk_rect + '\n')
        for k in pathes_new:
            svg.write(k + '\n')
        svg.write("</svg>")
    svg.close()


def golden_pattern(aa, element):
    """parse new design element"""
    doc = minidom.parse(element)
    pathes = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    path_color = [path.getAttribute('fill') for path in doc.getElementsByTagName('path')]
    bk_color = [path.getAttribute('fill') for path in doc.getElementsByTagName('rect')]
    pattern = []
    g_pattern = '<g id=' + '"pattern">'
    pattern.append(g_pattern)

    """add bk rect"""
    rect = '<rect width="' + str(13 * aa) + '" height="' + str(13 * aa) + '" fill="' + str(bk_color[0]) + '"/>'
    pattern.append(rect)

    """pattern1"""
    g1 = '<g id="pattern1" transform="' + 'matrix(1,0,0,1,' + str(int(0.81 * aa)) + ',' + str(int(0.81 * aa)) + ')">'
    pattern.append(g1)

    prop1 = 'transform="translate(0.000000,0.000000) scale(1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop1 + path_color[i] + '"/>')
    pattern.append('</g>')

    """pattern2"""
    g2 = '<g id="pattern2" transform="' + 'matrix(0.618,0,0,0.618,' + str(int(6.16 * aa)) + ',' \
         + str(int(1.81 * aa)) + ')">'
    pattern.append(g2)
    prop2 = 'transform="translate(' + str(int(8.16 * aa)) + \
            ',0.000000) scale(-1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop2 + path_color[i] + '"/>')
    pattern.append('</g>')

    """pattern3"""
    g3 = '<g id="pattern3" transform="' + 'matrix(0.618,0,0,0.618,' + str(int(1.31 * aa + aa)) + ',' + \
         str(int(8.16 * aa)) + ')matrix(0.71,0.71,-0.71,0.71,0,0)">'
    pattern.append(g3)
    prop3 = 'transform="translate(' + str(int(1.31 * aa)) + ',-' + str(int(1.31 * aa)) + \
            ') scale(1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop3 + path_color[i] + '"/>')
    pattern.append('</g>')

    """pattern4"""
    g4 = '<g id="pattern4" transform="' + 'matrix(1.618,0,0,1.618,' + str(int(5.54 / 1.618 * aa)) + ',' + \
         str(int(5.54 / 1.618 * aa)) + ')matrix(0.87,0.5,-0.5,0.87,0,0)">'
    pattern.append(g4)
    prop4 = 'transform="translate(' + str(int(1.31 * aa)) + ',-' + str(int(1.31 * aa)) + \
            ') scale(1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop4 + path_color[i] + '"/>')
    pattern.append('</g>')

    pattern.append('</g>')

    return pattern, bk_color



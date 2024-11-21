# -*- coding:utf-8 -*-
import math
from random import randint as ri
from random import uniform as rf
import lxml.etree as ET
from xml.dom import minidom
import time
import argparse
import sys
import random
from operator import itemgetter
import itertools
from collections import defaultdict, Counter
import numpy as np
import cv2  # 3.4.2
import imutils
import os
import cairosvg
from matplotlib import pyplot as plt

from utils.colorize_functions import rgb_to_hex, hex_to_rgb


def stripe_pathes(height, width_s, color, num):
    pathes = []
    loc_x = cal_loc(width_s)
    for i in range(len(width_s)):
        # 1. random color
        # rect_color = hex_random()
        # 2. from ref color image
        color_list = list(range(0, num))
        draw = draw_sequence(color_list)
        rect_color = rgb_to_hex(color[next(draw)])

        rect_path = '<rect x="' + str(loc_x[i]) + '" y="0" width="' + \
                    str(width_s[i]) + '" height="' + str(height) + \
                    '" fill="' + str(rect_color) + '"/>'

        pathes.append(rect_path)
    return pathes


def draw_sequence(sequence):
    sequence_copy = sequence[:]  
    random.shuffle(sequence_copy)  

    index = 0
    while True:
        yield sequence_copy[index]
        index += 1
        if index >= len(sequence_copy):
            random.shuffle(sequence_copy)
            index = 0


def cal_loc(ls):
    b = [0]
    for i in range(len(ls) - 1):
        _b = sum(ls[:i + 1])
        b.append(_b)
    return b


def cal_left(width, a):
    left = width - sum(a)
    return left


def generate_random_width(width, n):
    a0 = ri(10, int(width / n))
    a = [a0]
    for i in range(n - 2):
        left = cal_left(width, a)
        a1 = ri(0, left)
        a.append(a1)
    a_ = width - sum(a)
    a.append(a_)
    return a


def generate_new_svg(savename, header, pathes_new, new_bk_rect):
    with open(savename, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write('<metadata>\n'
                  'Created by ZoeQu, written in 2024\n'
                  '</metadata>\n')
        svg.write(new_bk_rect + '\n')
        for k in pathes_new:
            svg.write(k + '\n')
        svg.write("</svg>")
    svg.close()


def generate_golden_pattern(aa, element):
    # parse new design element
    doc = minidom.parse(element)
    pathes = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    path_color = [path.getAttribute('fill') for path in doc.getElementsByTagName('path')]
    bk_color = [path.getAttribute('fill') for path in doc.getElementsByTagName('rect')]
    
    pattern = []
    g_pattern = '<g id=' + '"pattern">'
    pattern.append(g_pattern)

    # add bk rect
    rect = '<rect width="' + str(13 * aa) + '" height="' + str(13 * aa) + '" fill="' + str(bk_color[0]) + '"/>'
    pattern.append(rect)

    # pattern1
    g1 = '<g id="pattern1" transform="' + 'matrix(1,0,0,1,' + str(int(0.81 * aa)) + ',' + str(int(0.81 * aa)) + ')">'
    pattern.append(g1)

    prop1 = 'transform="translate(0.000000,0.000000) scale(1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop1 + path_color[i] + '"/>')
    pattern.append('</g>')

    # pattern2
    g2 = '<g id="pattern2" transform="' + 'matrix(0.618,0,0,0.618,' + str(int(6.16 * aa)) + ',' \
         + str(int(1.81 * aa)) + ')">'
    pattern.append(g2)
    prop2 = 'transform="translate(' + str(int(8.16 * aa)) + \
            ',0.000000) scale(-1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop2 + path_color[i] + '"/>')
    pattern.append('</g>')

    # pattern3
    g3 = '<g id="pattern3" transform="' + 'matrix(0.618,0,0,0.618,' + str(int(1.31 * aa + aa)) + ',' + \
         str(int(8.16 * aa)) + ')matrix(0.71,0.71,-0.71,0.71,0,0)">'
    pattern.append(g3)
    prop3 = 'transform="translate(' + str(int(1.31 * aa)) + ',-' + str(int(1.31 * aa)) + \
            ') scale(1,1)" stroke="none" fill="'
    for i in range(len(pathes)):
        pattern.append('<path d="' + pathes[i] + '" ' + prop3 + path_color[i] + '"/>')
    pattern.append('</g>')

    # pattern4
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



def striperowgroup(pathes_new, width):
    rowgroup = []
    for i in range(5):
        grouppath = '<g id="' + str(i) + '" ' + 'transform=' + '"translate(' + \
                    str(i * width) + ',0)' + 'scale(1,1)' + '">' + '\n'
        rowgroup.append(grouppath)
        for j in pathes_new:
            rowgroup.append(j)
        rowgroup.append('</g>' + '\n')
    return rowgroup



def rowgroup(pathes_new, width):
    rowgroup = []
    for i in range(5):
        grouppath = '<g id="' + str(i) + '" ' + 'transform=' + '"translate(' + \
                    str(i * width) + ',0)' + 'scale(0.1,0.1)' + '">' + '\n'
        rowgroup.append(grouppath)
        for j in pathes_new:
            rowgroup.append(j)
        rowgroup.append('</g>' + '\n')
    return rowgroup



def columgroup(pathes_new, height):
    colgroup = []
    for i in range(5):
        grouppath = '<g id="' + str(i) + '" ' +\
                    'transform=' + '"translate(0,' +\
                    str(i * height) + ')' + 'scale(0.1,0.1)' + '">' + '\n'
        colgroup.append(grouppath)
        for j in pathes_new:
            colgroup.append(j)
        colgroup.append('</g>' + '\n')
    return colgroup



def mirror(element, width, height):
    doc = minidom.parse(element)
    path_info = [[path.getAttribute('d'), path.getAttribute('fill')]
                 for path in doc.getElementsByTagName('path')]
    bk_hex = [rect.getAttribute('fill') for rect
              in doc.getElementsByTagName('rect')]

    path_new = []
    # scale pattern 50%
    grouppath = '<g' + ' transform=' + '"matrix(0.5,0,0,0.5,0,0)"' + '>' + '\n' 
    path_new.append(grouppath)

    for i in path_info:
        path = i[0]
        fillcolor = i[1]
        path_ = '<path d="' + str(path) + '"' + ' transform="translate(' + str(0) + ',' + str(height) + ')'\
                + ' scale(0.1,-0.1)"' + ' stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
        path_new.append(path_)

    for i in path_info:
        path = i[0]
        fillcolor = i[1]
        path_ = '<path d="' + str(path) + '"' + ' transform="translate(' + str(2 * width) + ',' + str(height) + ')'\
                + ' scale(-0.1,-0.1)"' + ' stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
        path_new.append(path_)

    for i in path_info:
        path = i[0]
        fillcolor = i[1]
        path_ = '<path d="' + str(path) + '"' + ' transform="translate(' + str(0) + ',' + str(height) + ')'\
                + ' scale(0.1,0.1)"' + ' stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
        path_new.append(path_)

    for i in path_info:
        path = i[0]
        fillcolor = i[1]
        path_ = '<path d="' + str(path) + '"' + ' transform="translate(' + str(2 * width) + ',' + str(height) + ')'\
                + ' scale(-0.1,0.1)"' + ' stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
        path_new.append(path_)

    path_new.append('</g>' + '\n')
    return path_new


def patterngeneration(element, savename, type, header, patternwidth, patternheight, bk_rect, pathes_new):
    row = rowgroup(pathes_new, patternwidth / 4)
    col = columgroup(pathes_new, patternheight / 4)

    with open(savename, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write('<metadata>\n'
                  'Created by ZoeQu, written in 2024\n'
                  '</metadata>\n')
        svg.write(bk_rect + '\n')

        if type == 'straight':
            for r in range(4):
                svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                          '"translate(' + str(int(patternwidth / 30)) +
                          ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
                for k in row:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        if type == 'tile':
            for r in range(4):
                if (r % 2) == 0:
                    svg.write('<g id="row' + str(r) + '" ' +
                              'transform=' + '"translate(' + str(int(patternwidth / 30)) +
                              ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
                else:
                    svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                              '"translate(' + str(int(patternwidth / 30) - int(patternwidth / 8))
                              + ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
                for k in row:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        if type == 'half-drop':
            for c in range(4):
                if (c % 2) == 0:
                    svg.write('<g id="col' + str(c) + '" ' + 'transform=' +
                              '"translate(' + str(int(c * patternwidth / 4)) +
                              ', ' + str(int(patternheight / 30)) + ')' + '">' + '\n')
                else:
                    svg.write('<g id="col' + str(c) + '" ' +
                              'transform=' + '"translate(' + str(int(c * patternwidth / 4)) +
                              ', ' + str(int(patternheight / 30) - patternheight / 8) + ')' +
                              '">' + '\n')
                for k in col:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        if type == 'mirror':
            pathes_new = mirror(element, patternwidth, patternheight)
            row = rowgroup(pathes_new, patternwidth / 4)

            for r in range(4):
                svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                          '"translate(' + str(int(patternwidth / 30)) +
                          ',' + str(r * patternheight / 4) + ')' + '">' + '\n')
                for k in row:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        svg.write("</svg>")
    svg.close()



def temp_svg(path_i, header, temp_folder, width, height):
    # generate a svg file base on input svg path
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



def cal_area(tempname, width, height, color):
    # calculate the percentage of background color
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

        color = hex_to_rgb(j[1])
        colors.append(j[1])

        arearate = cal_area(temppng, width, height, color)
        os.remove(tempsvg)  # remove bk.svg
        os.remove(temppng)  # remove bk.png
        color_info.append([color, arearate])

    colors_ = set(colors)
    color_info_ = []
    for i in colors_:
        cc = hex_to_rgb(i)
        color_amount = 0
        for j in color_info:
            if j[0] == cc:
                color_amount += j[1]
        color_info_.append([i, color_amount])

    return color_info_


def read_svg(svg_name, temp_folder):
    # read svg's info
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

    # calculate path's area
    color_info_ = cal_svg_info(path_info, header, temp_folder, width, height)

    bk_area = 1
    for j in color_info_:
        bk_area -= j[1]
    color_info_.append([bk_hex[0], bk_area])
    color_info_ = sorted(color_info_, key=lambda k: k[1])

    doc.unlink()

    return color_info_, header, height, width, bk_hex, pathes



def pares_svg(element):
    doc = minidom.parse(element)

    # Extract height and width from the SVG element
    svg_tag = doc.getElementsByTagName('svg')[0]
    width = svg_tag.getAttribute('width')
    height = svg_tag.getAttribute('height')

    # Collect path and fill information
    path_info = [[path.getAttribute('d'), path.getAttribute('fill')]
                 for path in doc.getElementsByTagName('path')]
    fill_colors = {info[1] for info in path_info}
    # Collect background color information from rect elements
    bk_hex = [rect.getAttribute('fill') for rect
              in doc.getElementsByTagName('rect')]
    
    colors = list(fill_colors.union(bk_hex))

    path_new = []
    for i in path_info:
        path = i[0]
        fillcolor = i[1]
        path_ = '<path d="' + str(path) + '"' + ' transform="translate(0,' + str(height) + ')'\
                + ' scale(0.1,-0.1)"' + ' stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
        path_new.append(path_)

    return path_new, bk_hex, width, height, len(colors)


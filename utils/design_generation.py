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
from utils.func_read import read_svg
from utils.func_generate import golden_pattern


def rowgroup(pathes_new, width):
    rowgroup = []
    for i in range(5):
        grouppath = '<g id="' + str(i) + '" ' + 'transform=' + '"translate(' + \
                    str(i * width) + ',0)' + 'scale(1,1)' + '">' + '\n'
        rowgroup.append(grouppath)
        for j in pathes_new:
            rowgroup.append(j)
        rowgroup.append('</g>' + '\n')
    return rowgroup


def colgroup(pathes_new, height):
    colgroup = []
    for i in range(5):
        grouppath = '<g id="' + str(i) + '" ' +\
                    'transform=' + '"translate(0,' +\
                    str(i * height) + ')' + 'scale(0.8,0.8)' + '">' + '\n'
        colgroup.append(grouppath)
        for j in pathes_new:
            colgroup.append(j)
        colgroup.append('</g>' + '\n')
    return colgroup


def mirror(element, patternwidth, patterhheight):
    doc = minidom.parse(element)
    path_info = [[path.getAttribute('d'), path.getAttribute('fill')]
                 for path in doc.getElementsByTagName('path')]
    bk_hex = [rect.getAttribute('fill') for rect
              in doc.getElementsByTagName('rect')]

    width = patternwidth / 4
    height = patterhheight / 4

    path_new = []
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
    col = colgroup(pathes_new, patternheight / 4)

    with open(savename, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write('<metadata>\n'
                  'Created by ZoeQu, written in 2022\n'
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


def pares_svg(element, width, height):
    doc = minidom.parse(element)
    path_info = [[path.getAttribute('d'), path.getAttribute('fill')]
                 for path in doc.getElementsByTagName('path')]
    bk_hex = [rect.getAttribute('fill') for rect
              in doc.getElementsByTagName('rect')]

    path_new = []
    for i in path_info:
        path = i[0]
        fillcolor = i[1]
        path_ = '<path d="' + str(path) + '"' + ' transform="translate(0,' + str(height) + ')'\
                + ' scale(0.1,-0.1)"' + ' stroke="none" ' + 'fill="' + fillcolor + '"/>\n'
        path_new.append(path_)

    return path_new, bk_hex


def design_generate(width, height, generatePath, element):
    """
    new design generation
    :param width: input element width
    :param height: input element height
    :param generatePath: the save path
    :param element: input design element
    :return:
    """
    patternwidth = 4 * width
    patternheight = 4 * height
    patternheader = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="' \
                    + str(patternwidth) + 'pt" height="' + str(patternheight) + \
                    'pt" viewBox="' + '0 0 ' + str(patternwidth) + ' ' + \
                    str(patternheight) + '" ' + \
                    'preserveAspectRatio = "xMidYMid meet" >'

    pathes_new, bk_hex = pares_svg(element, width, height)
    bk_rect = '<rect width="' + str(patternwidth) + '" height="' + str(patternheight) + \
              '" fill="' + str(bk_hex[0]) + '"/>'

    for i in ['straight', 'tile', 'half-drop', 'mirror', 'customize-golden-ratio']:
        # i = 'customize-golden-ratio'
        if i != 'customize-golden-ratio':
            newpatternname = element[:-4] + '_' + str(i) + '_pattern.svg'
            patterngeneration(element, newpatternname, i, patternheader, patternwidth, patternheight, bk_rect, pathes_new)

        else:
            aa = int(10 * max(patternwidth / 4, patternheight / 4)/(1.618 * 1.618))
            pattern_path, bk_color = golden_pattern(aa, element)
            width2 = int(12 * aa)

            bk_rect_gold = '<rect width="' + str(width2) + '" height="' + str(width2) + \
                           '" fill="' + str(bk_color[0]) + '"/>'

            rowgroup = []
            for i in range(5):
                grouppath = '<g id="' + str(i) + '" ' + 'transform=' + '"translate(' + \
                            str(i * width2 * 0.25) + ',0)' + 'scale(0.25,0.25)' + '">' + '\n'
                rowgroup.append(grouppath)
                for j in pattern_path:
                    rowgroup.append(j)
                rowgroup.append('</g>' + '\n')

            newpatternname = element[:-4] + '_customize-golden-ratio_pattern.svg'
            header_gold = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="' \
                          + str(int(width2)) + 'pt" height="' + str(int(width2)) + \
                          'pt" viewBox="' + '0 0 ' + str(int(width2)) + ' ' + \
                          str(int(width2)) + '" ' + \
                          'preserveAspectRatio = "xMidYMid meet" >'
            with open(newpatternname, 'w') as svg:
                svg.write('<?xml version="1.0" standalone="no"?>\n'
                          '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                          ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
                svg.write(header_gold + '\n')
                svg.write('<metadata>\n'
                          'Created by ZoeQu, written in 2022\n'
                          '</metadata>\n')
                svg.write(bk_rect_gold + '\n')
                for r in range(4):
                    svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                              '"translate(' + str(int(0)) +
                              ',' + str(r * width2 / 4) + ')' + '">' + '\n')
                    for k in rowgroup:
                        svg.write(k + '\n')
                    svg.write('</g>' + '\n')

                svg.write("</svg>")
            svg.close()

